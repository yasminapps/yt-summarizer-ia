import pytest
from utils.formatter import clean_transcript

def test_clean_transcript_removes_extra_whitespace():
    raw = "This   is   a   test.\n\nWith    too   many spaces."
    cleaned = clean_transcript(raw)
    assert "  " not in cleaned
    assert "\n" not in cleaned
    assert cleaned.startswith("This is a test.")

def test_clean_transcript_removes_brackets_content():
    raw = "This is [MUSIC] a [NOISE] test."
    cleaned = clean_transcript(raw)
    assert "[MUSIC]" not in cleaned
    assert "[NOISE]" not in cleaned

def test_clean_transcript_is_truncated():
    long_text = "test " * 1000  # will exceed 3000 chars
    cleaned = clean_transcript(long_text, max_length=3000)
    assert len(cleaned) <= 3000
