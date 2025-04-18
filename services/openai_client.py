import requests
import json
import os
from dotenv import load_dotenv
from utils.decorators import safe_exec, log_execution, timed
from utils.dependency_injector import inject_dependencies
from utils.logger import Logger
from utils.config import Config

load_dotenv()

@timed
@log_execution
@safe_exec
@inject_dependencies
def call_openai_llm(
    prompt: str, 
    api_url: str = None, 
    api_key: str = None, 
    model: str = None,
    logger: Logger = None,
    config: Config = None
) -> dict:
    """
    Appelle l'API OpenAI (ou compatible) pour obtenir un résumé.
    Ne stocke pas la clé, ne log rien de sensible.
    
    Args:
        prompt: Le texte à soumettre à OpenAI
        api_url: URL de l'API OpenAI (défaut: valeur d'environnement)
        api_key: Clé API OpenAI (défaut: valeur d'environnement)
        model: Le modèle à utiliser (défaut: défini dans config)
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        dict: La réponse d'OpenAI avec le résumé et les infos sur les tokens
    """
    api_url = api_url or os.getenv("OPENAI_API_URL") or config.OPENAI_API_URL
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    model = model or config.OPENAI_MODEL

    # Masquer la clé API dans les logs
    masked_key = "***" if api_key else "non fournie"
    logger.debug(f"🤖 Appel OpenAI avec modèle: {model}, API Key: {masked_key}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Tu es un assistant qui résume du contenu."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    try:
        logger.debug(f"🛠️ Payload size: {len(str(data))} chars")
        logger.debug(f"🛠️ Prompt preview: {data['messages'][-1]['content'][:50]}")
        logger.debug(f"🛠️ Utilisation du modèle: {model}")
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        json_response = response.json()

        # Calculer les statistiques de tokens pour les logs
        total_tokens = json_response.get("usage", {}).get("total_tokens", 0) 
        prompt_tokens = json_response.get("usage", {}).get("prompt_tokens", 0)
        completion_tokens = json_response.get("usage", {}).get("completion_tokens", 0)
        
        logger.debug(f"📥 Réponse OpenAI reçue: {total_tokens} tokens au total " +
                    f"({prompt_tokens} prompt, {completion_tokens} réponse)")

        return {
            "response": json_response["choices"][0]["message"]["content"],
            "tokens_used": json_response.get("usage", {})
        }

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'appel à OpenAI: {str(e)}")
        return {
            "response": f"Erreur appel OpenAI : {str(e)}",
            "tokens_used": {}
        }
