import pytest
from services.youtube_transcript import extract_video_id, get_transcript_text
from youtube_transcript_api import YouTubeTranscriptApi
from unittest.mock import patch

def test_extract_video_id_valid_url():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert extract_video_id(url) == "dQw4w9WgXcQ"

def test_extract_video_id_short_url():
    url = "https://youtu.be/dQw4w9WgXcQ"
    assert extract_video_id(url) == "dQw4w9WgXcQ"

def test_extract_video_id_invalid_url():
    url = "https://example.com/watch?v=abc"
    assert extract_video_id(url) is None

@patch.object(YouTubeTranscriptApi, 'get_transcript')
def test_get_transcript_text(mock_get_transcript):
    mock_get_transcript.return_value = [
        {"text": "Hello"}, {"text": "world!"}
    ]
    result = get_transcript_text("https://www.youtube.com/watch?v=fakeid")
    assert result == "Hello\nworld!"