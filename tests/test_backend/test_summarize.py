import pytest
from flask import Flask
from routes.summarize import summarize
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.add_url_rule("/summarize", view_func=summarize, methods=["POST"])
    return app.test_client()

@pytest.fixture
def default_form_data():
    return {
        "youtube_url": "https://www.youtube.com/watch?v=drdNo6yfAUI",
        "summary_type": "full",
        "language": "en",
        "detail_level": "medium",
        "style": "mixed",
        "add_emojis": "yes",
        "add_tables": "yes",
        "specific_instructions": ""
    }

@pytest.fixture
def mock_dependencies():
    with patch("routes.summarize.get_llm_client") as mock_client, \
         patch("routes.summarize.get_transcript_text", return_value="Mocked transcript"), \
         patch("routes.summarize.split_transcript_by_tokens", return_value=["Chunk 1", "Chunk 2"]), \
         patch("routes.summarize.build_initial_prompt", return_value="Initial prompt"), \
         patch("routes.summarize.build_update_prompt", return_value="Updated prompt"):

        mock_llm = MagicMock()
        mock_llm.side_effect = [
            {"response": "Step 1 summary", "tokens_used": {"total_tokens": 100}, "execution_time": 2},
            {"response": "Final summary", "tokens_used": {"total_tokens": 200}, "execution_time": 4}
        ]
        mock_client.return_value = mock_llm

        yield

def test_summarize_missing_url(client):
    response = client.post("/summarize", data={})
    json_data = response.get_json()
    assert response.status_code in [400, 500]
    assert "URL YouTube invalide" in json_data["summary"]

def test_summarize_transcript_error(client):
    with patch("routes.summarize.get_transcript_text", side_effect=ValueError("Pas de transcript")):
        response = client.post("/summarize", data={"youtube_url": "https://test.com"})
        json_data = response.get_json()
        assert response.status_code in [400, 500]
        assert "Erreur" in json_data["summary"]

def test_summarize_successful_flow(client, default_form_data, mock_dependencies):
    response = client.post("/summarize", data=default_form_data)
    json_data = response.get_json()
    assert response.status_code in [200, 500]
    assert "Final summary" in json_data["summary"]
    assert json_data["transcript"] == "Mocked transcript"
    assert json_data["tokens"]["total_tokens"] == 200
    assert json_data["execution_time"] == 4

def test_prompt_empty_response(client, default_form_data):
    with patch("routes.summarize.get_transcript_text", return_value="Transcript"), \
         patch("routes.summarize.get_llm_client") as mock_client, \
         patch("routes.summarize.split_transcript_by_tokens", return_value=["chunk"]), \
         patch("routes.summarize.build_initial_prompt", return_value="initial"):

        mock_llm = MagicMock(return_value={"response": "", "tokens_used": {"total_tokens": 50}, "execution_time": 2})
        mock_client.return_value = mock_llm

        response = client.post("/summarize", data=default_form_data)
        json_data = response.get_json()
        assert response.status_code in [200, 500]
        assert isinstance(json_data["summary"], str)

def test_missing_user_api_key_with_engine_user(client, default_form_data):
    form_data = default_form_data.copy()
    form_data.update({
        "engine": "openai-user",
        "api_key": ""
    })

    with patch("routes.summarize.get_transcript_text", return_value="Transcript"), \
         patch("routes.summarize.get_llm_client") as mock_client, \
         patch("routes.summarize.split_transcript_by_tokens", return_value=["chunk"]), \
         patch("routes.summarize.build_initial_prompt", return_value="initial"):

        mock_llm = MagicMock(return_value={"response": "Summary", "tokens_used": {"total_tokens": 30}, "execution_time": 1})
        mock_client.return_value = mock_llm

        response = client.post("/summarize", data=form_data)
        json_data = response.get_json()
        assert response.status_code in [200, 500]
        assert "Summary" in json_data["summary"]

def test_split_transcript_returns_empty(client, default_form_data):
    with patch("routes.summarize.get_transcript_text", return_value="Transcript content"), \
         patch("routes.summarize.split_transcript_by_tokens", return_value=[]), \
         patch("routes.summarize.get_llm_client") as mock_client:

        mock_llm = MagicMock(return_value={"response": "Summary", "tokens_used": {}, "execution_time": 0})
        mock_client.return_value = mock_llm

        response = client.post("/summarize", data=default_form_data)
        json_data = response.get_json()
        assert response.status_code in [200, 500]
        assert json_data["summary"]

def test_summarize_generic_exception(client, default_form_data):
    with patch("routes.summarize.get_transcript_text", side_effect=Exception("unexpected error")):
        response = client.post("/summarize", data=default_form_data)
        json_data = response.get_json()
        assert response.status_code == 500
        assert "Erreur" in json_data["summary"]