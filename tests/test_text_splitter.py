import pytest
from services.text_splitter import split_transcript_by_tokens
from utils.config import config
import tiktoken

def test_split_transcript_empty():
    """Test que le texte vide retourne une liste vide"""
    assert split_transcript_by_tokens("") == []
    assert split_transcript_by_tokens(None) == []


def test_split_transcript_short_text():
    """Test qu'un texte court est retourné dans un seul élément"""
    short_text = "Ceci est un texte court qui ne sera pas divisé."
    result = split_transcript_by_tokens(short_text)
    assert len(result) == 1
    assert result[0] == short_text


def test_split_transcript_long_text():
    """Test qu'un texte long est divisé en plusieurs morceaux"""
    # Créer un texte suffisamment long pour être divisé
    long_text = ". ".join(["Phrase " + str(i) for i in range(10000)])
    
    result = split_transcript_by_tokens(long_text)
    assert len(result) > 1  # Doit être divisé en au moins 2 morceaux


def test_split_transcript_respects_max_tokens():
    """Test que la longueur max en tokens est respectée"""
    very_long_paragraph = " ".join(["This is a test."] * 10000)
    result = split_transcript_by_tokens(very_long_paragraph, max_tokens=config.MAX_TOKENS)

    encoding = tiktoken.encoding_for_model(config.OPENAI_MODEL)

    for chunk in result:
        token_count = len(encoding.encode(chunk))
        assert token_count <= config.MAX_TOKENS, f"Chunk with {token_count} tokens exceeds limit {config.MAX_TOKENS}"

