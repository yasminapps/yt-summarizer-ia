# services/text_splitter.py

import tiktoken


def split_transcript_by_tokens(text, max_tokens=10000, model="gpt-3.5-turbo"):
    """
    Coupe un texte en morceaux de max_tokens, en respectant les phrases si possible.

    Args:
        text (str): Le texte complet à découper
        max_tokens (int): Limite max de tokens par chunk
        model (str): Modèle utilisé pour le token count (ex: gpt-4o)

    Returns:
        List[str]: Liste des morceaux découpés
    """
    encoding = tiktoken.encoding_for_model(model)
    sentences = text.split('. ')  # Découpe basique par phrase (peut être améliorée)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        test_chunk = current_chunk + sentence + ". "
        tokens = len(encoding.encode(test_chunk))

        if tokens <= max_tokens:
            current_chunk = test_chunk
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks