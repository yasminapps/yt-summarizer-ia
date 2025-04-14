from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from utils.decorators import safe_exec, log_execution, timed

@timed
@log_execution
@safe_exec
def get_llm_client(engine, api_url="", api_key=""):
    """
    Retourne la fonction IA appropriée selon le choix utilisateur.
    - Si openai-user est sélectionné et clé + URL présentes → OpenAI (clé utilisateur)
    - Si openai-default est sélectionné → OpenAI avec clé du projet
    - Sinon, fallback Ollama
    """
    if engine == "openai-user" and api_url and api_key:
        def openai_wrapper(prompt):
            return call_openai_llm(prompt, api_url, api_key)
        return openai_wrapper

    if engine == "openai-default":
        def openai_default_wrapper(prompt):
            return call_openai_llm(prompt)  # utilisera les valeurs du .env
        return openai_default_wrapper
    
    # Par défaut, on utilise Ollama
    def ollama_wrapper(prompt):
        return call_ollama_llm(prompt)  # result est déjà un dict propre
    return ollama_wrapper