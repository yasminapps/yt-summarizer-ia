import pytest
from utils.input_sanitizer import (
    sanitize_url,
    sanitize_language,
    sanitize_engine_choice,
    sanitize_detail_level,
    sanitize_summary_type,
    sanitize_style,
    sanitize_boolean_choice,
    sanitize_api_url,
    sanitize_text_input,
    sanitize_form_data
)
from utils.config import config
import mock

# Tests pour sanitize_url
def test_sanitize_url_valid_youtube():
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=123"
    ]
    for url in valid_urls:
        assert sanitize_url(url) != ""

def test_sanitize_url_invalid():
    invalid_urls = [
        "https://www.example.com",
        "https://www.youtube.com/channel/123",
        "https://youtube.com/playlist?list=123",
        "invalid",
        "",
        "https://youtu.be/tooshort"
    ]
    for url in invalid_urls:
        assert sanitize_url(url) == ""

# Tests pour sanitize_language
def test_sanitize_language_valid():
    assert sanitize_language("en") == "en"
    assert sanitize_language("FR") == "fr"
    assert sanitize_language(" es ") == "es"

def test_sanitize_language_invalid():
    # Maintenant, la valeur par défaut vient de config.DEFAULT_LANGUAGE
    assert sanitize_language("invalid") == config.DEFAULT_LANGUAGE
    assert sanitize_language("") == config.DEFAULT_LANGUAGE
    assert sanitize_language("123") == config.DEFAULT_LANGUAGE

# Tests pour sanitize_engine_choice
def test_sanitize_engine_choice_valid():
    assert sanitize_engine_choice("ollama") == "ollama"
    assert sanitize_engine_choice("openai-user") == "openai-user"
    assert sanitize_engine_choice(" openai-default ") == "openai-default"

def test_sanitize_engine_choice_invalid():
    assert sanitize_engine_choice("invalid") == "openai-default"  # Valeur par défaut
    assert sanitize_engine_choice("") == "openai-default"
    assert sanitize_engine_choice("azure") == "openai-default"

def test_sanitize_engine_choice_with_custom_default():
    assert sanitize_engine_choice("invalid", default="openai-default") == "openai-default"
    assert sanitize_engine_choice("", default="openai-default") == "openai-default"
    assert sanitize_engine_choice("not-a-valid-engine", default="openai-user") == "openai-user"

# Tests pour sanitize_detail_level
def test_sanitize_detail_level_valid():
    assert sanitize_detail_level("short") == "short"
    assert sanitize_detail_level("medium") == "medium"
    assert sanitize_detail_level("detailed") == "detailed"

def test_sanitize_detail_level_invalid():
    # Maintenant, la valeur par défaut vient de config.DEFAULT_DETAIL_LEVEL
    assert sanitize_detail_level("invalid") == config.DEFAULT_DETAIL_LEVEL
    assert sanitize_detail_level("") == config.DEFAULT_DETAIL_LEVEL
    assert sanitize_detail_level("very-long") == config.DEFAULT_DETAIL_LEVEL

# Tests pour sanitize_summary_type
def test_sanitize_summary_type_valid():
    assert sanitize_summary_type("full") == "full"
    assert sanitize_summary_type("tools") == "tools"
    assert sanitize_summary_type("insights") == "insights"

def test_sanitize_summary_type_invalid():
    # Maintenant, la valeur par défaut vient de config.DEFAULT_SUMMARY_TYPE
    assert sanitize_summary_type("invalid") == config.DEFAULT_SUMMARY_TYPE
    assert sanitize_summary_type("") == config.DEFAULT_SUMMARY_TYPE
    assert sanitize_summary_type("summary") == config.DEFAULT_SUMMARY_TYPE

# Tests pour sanitize_style
def test_sanitize_style_valid():
    assert sanitize_style("bullet_points") == "bullet_points"
    assert sanitize_style("mixed") == "mixed"
    assert sanitize_style("text_only") == "text_only"

def test_sanitize_style_invalid():
    assert sanitize_style("invalid") == "mixed"
    assert sanitize_style("") == "mixed"
    assert sanitize_style("both") == "mixed"

# Tests pour sanitize_boolean_choice
def test_sanitize_boolean_choice_yes():
    assert sanitize_boolean_choice("yes") == "yes"

def test_sanitize_boolean_choice_no():
    assert sanitize_boolean_choice("no") == "no"
    assert sanitize_boolean_choice("false") == "no"
    assert sanitize_boolean_choice("0") == "no"
    assert sanitize_boolean_choice("") == "no"
    assert sanitize_boolean_choice("invalid") == "no"
    assert sanitize_boolean_choice("YES") == "no"
    assert sanitize_boolean_choice("true") == "no"
    assert sanitize_boolean_choice("1") == "no"
    assert sanitize_boolean_choice("oui") == "no"

# Tests pour sanitize_api_url
def test_sanitize_api_url_valid():
    valid_urls = [
        "https://api.openai.com/v1/completions",
        "https://api.example.com/endpoint",
        "http://localhost:8080/api"
    ]
    for url in valid_urls:
        assert sanitize_api_url(url) != ""

def test_sanitize_api_url_invalid():
    invalid_urls = [
        "not-a-url",
        "https://.com",
        "file:///etc/passwd",
        "",
        "ftp://example.com"
    ]
    for url in invalid_urls:
        assert sanitize_api_url(url) == ""

# Tests pour sanitize_text_input
def test_sanitize_text_input_normal():
    text = "This is a normal text with punctuation: 123, 456!"
    assert sanitize_text_input(text) == text

def test_sanitize_text_input_with_dangerous_chars():
    text = "Script <script>alert('XSS')</script> injection"
    sanitized = sanitize_text_input(text)
    assert "<script>" not in sanitized
    assert "alert" in sanitized
    assert "XSS" in sanitized

def test_sanitize_text_input_long_text():
    long_text = "a" * 10500
    sanitized = sanitize_text_input(long_text)
    assert len(sanitized) == 10000  # max_length par défaut

# Tests pour sanitize_form_data
def test_sanitize_form_data_complete():
    form_data = {
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "engine": "openai-user",
        "language": "fr",
        "detail_level": "detailed",
        "summary_type": "insights",
        "style": "mixed",
        "add_emojis": "yes",
        "add_tables": "no",
        "api_url": "https://api.openai.com/v1/completions",
        "api_key": "sk-1234567890abcdef",
        "specific_instructions": "Focus on key lessons."
    }
    
    sanitized = sanitize_form_data(form_data)
    
    assert sanitized["youtube_url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert sanitized["engine"] == "openai-user"
    assert sanitized["language"] == "fr"
    assert sanitized["detail_level"] == "detailed"
    assert sanitized["summary_type"] == "insights"
    assert sanitized["style"] == "mixed"
    assert sanitized["add_emojis"] == "yes"
    assert sanitized["add_tables"] == "no"
    assert sanitized["api_url"] == "https://api.openai.com/v1/completions"
    assert sanitized["api_key"] == "sk-1234567890abcdef"
    assert "Focus on key lessons" in sanitized["specific_instructions"]

def test_sanitize_form_data_with_invalid_data():
    form_data = {
        "youtube_url": "not-a-youtube-url",
        "engine": "invalid-engine",
        "language": "invalid-language",
        "api_url": "not-a-url"
    }
    
    sanitized = sanitize_form_data(form_data)
    
    assert sanitized["youtube_url"] == ""
    assert sanitized["engine"] == "openai-default"
    assert sanitized["language"] == config.DEFAULT_LANGUAGE
    assert sanitized["api_url"] == "" 