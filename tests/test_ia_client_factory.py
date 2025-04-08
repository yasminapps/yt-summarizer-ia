import pytest
from services.ia_client_factory import get_llm_client

def mock_openai(prompt, api_url=None, api_key=None):
    return {"response": f"openai: {prompt}", "tokens_used": {"prompt_tokens": 5}}

def mock_ollama(prompt):
    return f"ollama: {prompt}"

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