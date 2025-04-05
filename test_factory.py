from services.ia_client_factory import get_ia_client

# --- Cas 1 : OpenAI sélectionné, avec clé et URL ---
form_openai = {
    "engine": "openai",
    "api_key": "sk-test...",
    "api_url": "https://api.openai.com/v1/chat/completions"
}

client = get_ia_client(form_openai)
print("✅ Cas OpenAI →", client.__name__ if hasattr(client, '__name__') else "wrapper (fonction inline)")

# --- Cas 2 : Ollama par défaut ---
form_ollama = {
    "engine": "ollama"  # ou même aucun champ
}

client2 = get_ia_client(form_ollama)
print("✅ Cas Ollama →", client2.__name__)
