import pytest
from services.youtube_transcript import get_transcript_text
from utils.count_tokens import count_tokens
from services.text_splitter import split_transcript_by_tokens
import tiktoken

@pytest.mark.parametrize("prompt_path, title", [
    ("prompts/prompt_yt_summary.md", "Prompt de base"),
])
def test_count_tokens_from_prompt_file(prompt_path, title):
    with open(prompt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    tokens = count_tokens(content)
    print(f"{title} → {tokens} tokens")
    assert tokens > 0

def test_split_transcript_by_tokens():
    text = "Phrase 1. Phrase 2. Phrase 3. " * 1000  # Un très long texte
    chunks = split_transcript_by_tokens(text, max_tokens=10000)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} : {len(tiktoken.encoding_for_model('gpt-4o').encode(chunk))} tokens")

    assert all(len(tiktoken.encoding_for_model('gpt-4o').encode(c)) <= 10000 for c in chunks)