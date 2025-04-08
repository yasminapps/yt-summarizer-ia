import pytest
from unittest.mock import patch, Mock
from services.openai_client import call_openai_llm


@patch("services.openai_client.requests.post")
def test_openai_success(mock_post):
    # Simule une réponse valide de l'API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {"content": "Voici le résumé."}
        }],
        "usage": {"total_tokens": 42}
    }
    mock_post.return_value = mock_response

    result = call_openai_llm("Résumé ce texte", api_url="https://fake.url", api_key="sk-test")
    assert "Voici le résumé." in result["response"]
    assert result["tokens_used"]["total_tokens"] == 42


@patch("services.openai_client.requests.post")
def test_openai_invalid_api_key(mock_post):
    # Simule une erreur HTTP 401
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
    mock_post.return_value = mock_response

    result = call_openai_llm("Prompt", api_url="https://fake.url", api_key="wrong-key")
    assert "Erreur appel OpenAI" in result["response"]


@patch("services.openai_client.requests.post")
def test_openai_bad_url(mock_post):
    # Simule une erreur réseau
    mock_post.side_effect = Exception("Invalid URL")

    result = call_openai_llm("Prompt", api_url="bad-url", api_key="sk-xxx")
    assert "Erreur appel OpenAI" in result["response"]