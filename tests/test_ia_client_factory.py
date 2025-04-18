import pytest
from services.ia_client_factory import get_llm_client

def mock_openai(prompt, **kwargs):
    return {"response": f"openai: {prompt}", "tokens_used": {"prompt_tokens": 5}}

def mock_ollama(prompt, **kwargs):
    return {"response": f"ollama: {prompt}", "tokens_used": {}, "execution_time": 0.0}

# Patch les fonctions pour les tests
def test_get_llm_client_openai_user(monkeypatch):
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    client = get_llm_client("openai-user", api_url="http://fake.url", api_key="fake-key")
    result = client("test prompt")
    assert result["response"].startswith("openai:")

def test_get_llm_client_openai_default(monkeypatch):
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    client = get_llm_client("openai-default")
    result = client("test prompt")
    assert result["response"].startswith("openai:")

def test_get_llm_client_ollama(monkeypatch):
    monkeypatch.setattr("services.ia_client_factory.call_ollama_llm", mock_ollama)
    client = get_llm_client("ollama")
    result = client("test prompt")
    assert result["response"].startswith("ollama:")