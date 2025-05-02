import pytest
from services.youtube_transcript import extract_video_id, get_transcript_text
from unittest.mock import patch, MagicMock

def test_extract_video_id_standard_url():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"

def test_extract_video_id_short_url():
    url = "https://youtu.be/dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"

def test_extract_video_id_url_with_parameters():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120s"
    video_id = extract_video_id(url)
    assert video_id == "dQw4w9WgXcQ"

def test_extract_video_id_invalid_url():
    urls = [
        "https://www.google.com", 
        "https://youtube.com/channel/123", 
        "invalid", 
        ""
    ]
    for url in urls:
        video_id = extract_video_id(url)
        assert video_id is None

def test_extract_video_id_handles_exception():
    with patch('services.youtube_transcript.urlparse', side_effect=Exception('Test error')):
        video_id = extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert video_id is None

@patch('services.youtube_transcript.YouTubeTranscriptApi')
def test_get_transcript_text_success(mock_api_class):
    mock_api_instance = MagicMock()
    mock_api_class.return_value = mock_api_instance

    mock_api_instance.get_transcript.return_value = [
        {'text': 'First line of transcript', 'duration': 1.5},
        {'text': 'Second line of transcript', 'duration': 2.0}
    ]
    
    text = get_transcript_text("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    mock_api_instance.get_transcript.assert_called_once_with("dQw4w9WgXcQ", languages=['fr', 'en'])
    assert text == "First line of transcript\nSecond line of transcript"

@patch('services.youtube_transcript.extract_video_id')
def test_get_transcript_text_invalid_url(mock_extract):
    mock_extract.return_value = None
    
    with pytest.raises(ValueError, match="Lien YouTube invalide."):
        get_transcript_text("invalid url")

@patch('services.youtube_transcript.YouTubeTranscriptApi')
@patch('services.youtube_transcript.extract_video_id')
def test_get_transcript_text_custom_languages(mock_extract, mock_api_class):
    mock_extract.return_value = "dQw4w9WgXcQ"
    
    mock_api_instance = MagicMock()
    mock_api_class.return_value = mock_api_instance
    mock_api_instance.get_transcript.return_value = [{'text': 'Transcript text', 'duration': 1.0}]
    
    text = get_transcript_text("https://www.youtube.com/watch?v=dQw4w9WgXcQ", languages=['es', 'de'])

    mock_api_instance.get_transcript.assert_called_once_with("dQw4w9WgXcQ", languages=['es', 'de'])
    assert text == "Transcript text"