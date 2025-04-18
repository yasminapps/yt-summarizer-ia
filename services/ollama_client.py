import requests
import json
from utils.decorators import safe_exec, log_execution, timed
from utils.dependency_injector import inject_dependencies
from utils.logger import Logger
from utils.config import Config

@timed
@log_execution
@safe_exec
@inject_dependencies
def call_ollama_llm(
    prompt: str, 
    model: str = "llama3", 
    stream: bool = False,
    logger: Logger = None,
    config: Config = None
) -> dict:
    """
    Envoie une requête à Ollama pour générer un résumé.
    
    Args:
        prompt: Le texte à soumettre à Ollama
        model: Le modèle à utiliser (défaut: défini dans config)
        stream: Si True, utilise le streaming pour la réponse
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        dict: La réponse d'Ollama avec le résumé et les infos sur les tokens
    """
    # Utiliser le modèle par défaut de la config si non spécifié
    model = model or "llama3"
    
    url = "http://localhost:11434/api/generate"
    logger.debug(f"🦙 Appel Ollama avec modèle: {model}")

    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    headers = {"Content-Type": "application/json"}

    try:
        logger.debug(f"📤 Envoi de la requête Ollama (longueur prompt: {len(prompt)} caractères)")
        response = requests.post(url, data=json.dumps(data), headers=headers, stream=stream)
        response.raise_for_status()

        if stream:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = json.loads(line.decode("utf-8"))
                    full_response += decoded_line.get("response", "")
            result = full_response
        else:
            result = response.json().get("response", "")
            
        logger.debug(f"📥 Réponse Ollama reçue (longueur: {len(result)} caractères)")
        return {
            "response": result,
            "tokens_used": {}  # Ollama ne fournit pas les tokens
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'appel à Ollama: {str(e)}")
        return {
            "response": f"Erreur lors de l'appel à Ollama : {str(e)}",
            "tokens_used": {}
        }
