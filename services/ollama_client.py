import requests
import json
from utils.decorators import safe_exec, log_execution, timed

@timed
@log_execution
@safe_exec
def call_ollama_llm(prompt: str, model: str = "llama3", stream: bool = False) -> str:
    """
    Envoie une requête à Ollama pour générer un résumé.
    """
    url = "http://localhost:11434/api/generate"

    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, stream=stream)
        response.raise_for_status()

        if stream:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = json.loads(line.decode("utf-8"))
                    full_response += decoded_line.get("response", "")
            return full_response
        else:
            return response.json().get("response", "")
        
    except Exception as e:
        return f"Erreur lors de l’appel à Ollama : {str(e)}"
