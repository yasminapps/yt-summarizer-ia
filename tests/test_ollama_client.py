import pytest
from unittest.mock import patch, Mock
from services.ollama_client import call_ollama_llm


@patch("services.ollama_client.requests.post")
def test_ollama_success(mock_post):
    # Simule une réponse normale avec stream désactivé
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Résumé généré avec succès."}
    mock_post.return_value = mock_response

    result = call_ollama_llm("Voici le texte à résumer.")
    assert "Résumé généré" in result


@patch("services.ollama_client.requests.post")
def test_ollama_streaming(mock_post):
    # Simule une réponse en mode stream
    mock_response = Mock()
    mock_response.iter_lines.return_value = [
        b'{"response": "Bonjour"}',
        b'{"response": " tout"}',
        b'{"response": " le monde"}'
    ]
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = call_ollama_llm("Texte pour stream", stream=True)
    assert result == "Bonjour tout le monde"


@patch("services.ollama_client.requests.post")
def test_ollama_error(mock_post):
    # Simule une exception (ex: serveur non disponible)
    mock_post.side_effect = Exception("Connection refused")

    result = call_ollama_llm("Texte", model="llama3")
    assert "Erreur lors de l’appel à Ollama" in result