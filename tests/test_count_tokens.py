import pytest
from services.youtube_transcript import get_transcript_text
from utils.count_tokens import count_tokens
from services.text_splitter import split_transcript_by_tokens
import tiktoken

@pytest.mark.parametrize("youtube_url, title", [
    ("https://youtu.be/pc5A9-kWeeA?si=cStRgPhEyxW5wG0T", "Video 1"),
    ("https://youtu.be/drdNo6yfAUI?si=ZkMQeYef4uGDIfTM", "Video 2"),
    ("https://youtu.be/MOlO1_mj1dU?si=zIIL4upyiphRJaq0", "Video 3"),
    ("https://youtu.be/YWjRHYMxXWg?si=zmXd6vgAc4Buf2LY", "Video 4"),
])
def test_count_tokens_for_youtube_transcripts(youtube_url, title):
    transcript = get_transcript_text(youtube_url)
    tokens = count_tokens(transcript)
    print(f"{title} → {tokens} tokens")
    assert tokens > 0  # On vérifie que ça a bien compté les tokens

def test_split_transcript_by_tokens():
    text = "Phrase 1. Phrase 2. Phrase 3. " * 1000  # Un très long texte
    chunks = split_transcript_by_tokens(text, max_tokens=10000)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} : {len(tiktoken.encoding_for_model('gpt-4o').encode(chunk))} tokens")

    assert all(len(tiktoken.encoding_for_model('gpt-4o').encode(c)) <= 10000 for c in chunks)