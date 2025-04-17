# services/text_splitter.py

import tiktoken


def split_transcript_by_tokens(text, max_tokens=10000, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    sentences = text.split('.')  # très simple, à améliorer si besoin
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_with_dot = sentence + "."
        sentence_tokens = len(encoding.encode(sentence_with_dot))
        current_tokens = len(encoding.encode(current_chunk))

        # 🚨 Cas limite : phrase seule trop longue
        if sentence_tokens > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            chunks.append(sentence_with_dot.strip())  # phrase seule = chunk
            continue

        # ✅ Sinon, on ajoute si ça passe
        if current_tokens + sentence_tokens <= max_tokens:
            current_chunk += sentence_with_dot
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence_with_dot

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks