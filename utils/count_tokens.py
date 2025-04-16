from tiktoken import get_encoding

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Compte les tokens d'un texte selon le modèle OpenAI.
    """
    encoding = get_encoding("cl100k_base")  # adapté à GPT-3.5 & GPT-4
    return len(encoding.encode(text))