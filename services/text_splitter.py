# services/text_splitter.py

import tiktoken
from utils.count_tokens import count_tokens
from utils.logger import get_logger
from utils.config import config
from utils.dependency_injector import inject_dependencies

@inject_dependencies
def split_transcript_by_tokens(text, max_tokens=config.MAX_TOKENS, model=config.OPENAI_ENCODING_MODEL, logger=None, config=None):
    if not isinstance(text, str) or not text.strip():
        return []

    # Utiliser la configuration injectée si disponible
    max_tokens = max_tokens or getattr(config, 'MAX_TOKENS', 10000)
    model = model or getattr(config, 'OPENAI_ENCODING_MODEL', 'gpt-3.5-turbo')

    if logger:
        logger.debug(f"🔢 Splitting text with max_tokens={max_tokens}, model={model}")

    encoding = tiktoken.encoding_for_model(model)
    sentences = text.split('.')  # peut être amélioré plus tard
    chunks = []
    current_chunk = ""

    for sentence in sentences:
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

    if logger:
        logger.debug(f"✂️ Text split into {len(chunks)} chunks")

    return chunks