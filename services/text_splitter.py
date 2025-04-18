# services/text_splitter.py

import tiktoken
from utils.count_tokens import count_tokens
from utils.logger import Logger
from utils.config import Config
from utils.dependency_injector import inject_dependencies

@inject_dependencies
def split_transcript_by_tokens(
    text, 
    max_tokens=None, 
    model=None,
    logger: Logger = None,
    config: Config = None
):
    """
    Divise un texte en chunks qui ne dépassent pas le nombre maximal de tokens.
    
    Args:
        text: Le texte à diviser
        max_tokens: Nombre maximal de tokens par chunk (défaut: config.MAX_TOKENS)
        model: Modèle à utiliser pour l'encodage (défaut: config.OPENAI_ENCODING_MODEL)
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        list: Liste de chunks de texte
    """
    max_tokens = max_tokens or config.MAX_TOKENS
    model = model or config.OPENAI_ENCODING_MODEL
    
    if not isinstance(text, str) or not text.strip():
        logger.warning("⚠️ Tentative de division d'un texte vide ou invalide")
        return []

    logger.debug(f"📏 Fractionnement du texte en chunks (max tokens: {max_tokens}, modèle: {model})")
    
    try:
        encoding = tiktoken.encoding_for_model(model)
        sentences = text.split('.')  # peut être amélioré plus tard
        chunks = []
        current_chunk = ""
        
        total_sentences = len(sentences)
        logger.debug(f"🔍 {total_sentences} phrases à traiter")

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            sentence_with_dot = sentence + "."
            sentence_tokens = len(encoding.encode(sentence_with_dot))

            # 🚨 Cas limite : phrase trop longue à elle seule
            if sentence_tokens > max_tokens:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                chunks.append(sentence_with_dot.strip())
                logger.debug(f"⚠️ Phrase {i+1}/{total_sentences} trop longue ({sentence_tokens} tokens), ajoutée comme chunk séparé")
                continue

            # ✅ Vérifier si le chunk + la phrase tiennent dans la limite
            temp_chunk = current_chunk + sentence_with_dot
            temp_token_count = len(encoding.encode(temp_chunk))

            if temp_token_count <= max_tokens:
                current_chunk = temp_chunk
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence_with_dot

        if current_chunk:
            chunks.append(current_chunk.strip())

        logger.debug(f"✅ Texte divisé en {len(chunks)} chunks")
        return chunks
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la division du texte: {str(e)}")
        # En cas d'erreur, retourner le texte entier dans un seul chunk
        return [text]