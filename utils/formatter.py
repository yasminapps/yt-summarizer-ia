import re

def clean_transcript(raw_text: str, max_length: int = 3000) -> str:
    """
    Nettoie le transcript brut extrait de YouTube :
    - supprime les blancs excessifs
    - retire les balises, caractères spéciaux, etc.
    - limite la taille du texte pour éviter de surcharger l'IA
    """

    # Supprimer les multiples sauts de ligne / espaces
    cleaned = re.sub(r'\s+', ' ', raw_text)

    # Supprimer les caractères inutiles (ajustable)
    cleaned = re.sub(r'\[.*?\]', '', cleaned)  # [MUSIC], [LAUGHS], etc.

    # Tronquer si trop long (pour Ollama / OpenAI)
    return cleaned.strip()[:max_length]
