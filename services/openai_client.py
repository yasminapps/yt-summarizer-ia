import requests
import json

def call_openai_llm(prompt: str, api_url: str, api_key: str, model: str = "gpt-3.5-turbo") -> dict:
    """
    Appelle l'API OpenAI (ou compatible) pour obtenir un résumé.
    Ne stocke pas la clé, ne log rien de sensible.
    """

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
