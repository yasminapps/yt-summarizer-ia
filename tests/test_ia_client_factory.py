import pytest
from services.ia_client_factory import get_llm_client
from utils.config import config

def mock_openai(prompt, **kwargs):
    # Capturer les paramètres pour les tests
    mock_openai.last_kwargs = kwargs
    return {"response": f"openai: {prompt}", "tokens_used": {"prompt_tokens": 5}}

def mock_ollama(prompt, **kwargs):
    return {"response": f"ollama: {prompt}", "tokens_used": {}, "execution_time": 0.0}

# Patch les fonctions pour les tests
def test_get_llm_client_openai_user(monkeypatch):
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    client = get_llm_client("openai-user", api_url="http://fake.url", api_key="fake-key")
    result = client("test prompt")
    assert result["response"].startswith("openai:")
    
    # Vérifier que la fonction a reçu les bons paramètres
    assert mock_openai.last_kwargs["api_key"] == "fake-key"
    assert mock_openai.last_kwargs["api_base"] == "http://fake.url"

def test_get_llm_client_openai_default(monkeypatch):
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    client = get_llm_client("openai-default")
    result = client("test prompt")
    assert result["response"].startswith("openai:")
    
    # Vérifier que le modèle spécifié dans config est utilisé
    if hasattr(mock_openai, 'last_kwargs') and 'model' in mock_openai.last_kwargs:
        assert mock_openai.last_kwargs["model"] == config.OPENAI_MODEL

def test_get_llm_client_ollama(monkeypatch):
    monkeypatch.setattr("services.ia_client_factory.call_ollama_llm", mock_ollama)
    client = get_llm_client("ollama")
    result = client("test prompt")
    assert result["response"].startswith("ollama:")

def test_get_llm_client_with_config_values(monkeypatch):
    """Test que les valeurs de config sont utilisées correctement"""
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    
    # Sauvegarder les valeurs originales
    original_model = config.OPENAI_MODEL
    
    try:
        # Modifier temporairement la configuration
        config.OPENAI_MODEL = "test-model-from-config"
        
        client = get_llm_client("openai-user", api_key="test-key")
        result = client("test prompt")
        
        # Vérifier que le modèle de config est bien utilisé
        if hasattr(mock_openai, 'last_kwargs') and 'model' in mock_openai.last_kwargs:
            assert mock_openai.last_kwargs["model"] == "test-model-from-config"
    
    finally:
        # Restaurer les valeurs originales
        config.OPENAI_MODEL = original_model