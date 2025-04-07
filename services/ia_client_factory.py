from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm

def get_llm_client(engine, api_url="", api_key=""):
    """
    Retourne la fonction IA appropriée selon le choix utilisateur.
    - Si openai est sélectionné et clé + URL présentes → OpenAI
    - Sinon, fallback Ollama
    """
    if engine == "openai" and api_url and api_key:
        def openai_wrapper(prompt):
            return call_openai_llm(prompt, api_url, api_key)
        return openai_wrapper

    def ollama_wrapper(prompt):
        return {
            "response": call_ollama_llm(prompt),
            "tokens_used": {}
        }
    return ollama_wrapper
