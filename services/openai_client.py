import requests
import json
import os
from dotenv import load_dotenv
from utils.decorators import safe_exec, log_execution, timed
from utils.logger import get_logger
from utils.config import config

load_dotenv()

logger = get_logger()

@timed
@log_execution
@safe_exec
def call_openai_llm(prompt: str, api_url: str = None, api_key: str = None, model: str = config.OPENAI_MODEL) -> dict:
    """
    Appelle l'API OpenAI (ou compatible) pour obtenir un résumé.
    Ne stocke pas la clé, ne log rien de sensible.
    """
    api_url = api_url or os.getenv("OPENAI_API_URL") 
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    model = model or config.OPENAI_MODEL

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

        return {
            "response": json_response["choices"][0]["message"]["content"],
            "tokens_used": json_response.get("usage", {})
        }

    except Exception as e:
        return {
            "response": f"Erreur appel OpenAI : {str(e)}",
            "tokens_used": {}
        }
