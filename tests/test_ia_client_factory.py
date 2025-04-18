import pytest
from services.ia_client_factory import get_llm_client
from utils.config import Config
from utils.logger import Logger
from unittest.mock import MagicMock

def mock_openai(prompt, **kwargs):
    # Capturer les paramètres pour les tests
    mock_openai.last_kwargs = kwargs
    return {"response": f"openai: {prompt}", "tokens_used": {"prompt_tokens": 5}}

def mock_ollama(prompt, **kwargs):
    return {"response": f"ollama: {prompt}", "tokens_used": {}, "execution_time": 0.0}

# Mock config et logger pour les tests
@pytest.fixture
def mock_dependencies():
    mock_config = MagicMock(spec=Config)
    mock_config.OPENAI_MODEL = "gpt-4o"
    mock_config.ALLOWED_ENGINES = ["ollama", "openai-user", "openai-default"]
    
    mock_logger = MagicMock(spec=Logger)
    
    return mock_config, mock_logger

# Patch les fonctions pour les tests
def test_get_llm_client_openai_user(monkeypatch, mock_dependencies):
    mock_config, mock_logger = mock_dependencies
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    
    client = get_llm_client(
        "openai-user", 
        api_url="http://fake.url", 
        api_key="fake-key",
        logger=mock_logger,
        config=mock_config
    )
    
    result = client("test prompt")
    assert result["response"].startswith("openai:")
    
    # Vérifier que la fonction a reçu les bons paramètres
    assert mock_openai.last_kwargs["api_key"] == "fake-key"
    assert mock_openai.last_kwargs["api_url"] == "http://fake.url"

def test_get_llm_client_openai_default(monkeypatch, mock_dependencies):
    mock_config, mock_logger = mock_dependencies
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    
    client = get_llm_client(
        "openai-default",
        logger=mock_logger,
        config=mock_config
    )
    
    result = client("test prompt")
    assert result["response"].startswith("openai:")
    
    # Vérifier que le modèle spécifié dans config est utilisé
    if hasattr(mock_openai, 'last_kwargs') and 'model' in mock_openai.last_kwargs:
        assert mock_openai.last_kwargs["model"] == mock_config.OPENAI_MODEL

def test_get_llm_client_ollama(monkeypatch, mock_dependencies):
    mock_config, mock_logger = mock_dependencies
    monkeypatch.setattr("services.ia_client_factory.call_ollama_llm", mock_ollama)
    
    client = get_llm_client(
        "ollama",
        logger=mock_logger,
        config=mock_config
    )
    
    result = client("test prompt")
    assert result["response"].startswith("ollama:")

def test_get_llm_client_with_config_values(monkeypatch, mock_dependencies):
    """Test que les valeurs de config sont utilisées correctement"""
    mock_config, mock_logger = mock_dependencies
    monkeypatch.setattr("services.ia_client_factory.call_openai_llm", mock_openai)
    
    # Modifier le modèle dans la config mock
    mock_config.OPENAI_MODEL = "test-model-from-config"
    
    client = get_llm_client(
        "openai-user", 
        api_key="test-key",
        logger=mock_logger,
        config=mock_config
    )
    
    result = client("test prompt")
    
    # Vérifier que le modèle de config est bien utilisé
    if hasattr(mock_openai, 'last_kwargs') and 'model' in mock_openai.last_kwargs:
        assert mock_openai.last_kwargs["model"] == "test-model-from-config"