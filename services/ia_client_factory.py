from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm

def get_ia_client(form_data):
    """
    Retourne la fonction IA appropriée selon le choix utilisateur.
    - Si openai est sélectionné et clé + URL présentes → OpenAI
    - Sinon, fallback Ollama
    """
    engine = form_data.get("engine", "ollama")
    api_url = form_data.get("api_url", "").strip()
    api_key = form_data.get("api_key", "").strip()

    if engine == "openai" and api_url and api_key:
        def wrapper(prompt):
            return call_openai_llm(prompt, api_url, api_key)
        return wrapper

    return call_ollama_llm
