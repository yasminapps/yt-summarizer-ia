import pytest
from services.prompt_builder import (
    build_common_instructions, 
    build_final_prompt, 
    build_initial_prompt, 
    build_update_prompt,
    BASE_PROMPT
)
from unittest.mock import patch, MagicMock

# Fixtures
@pytest.fixture
def minimal_user_choices():
    return {
        "language": "en",
        "detail_level": "medium",
        "summary_type": "full",
        "style": "mixed",
        "add_emojis": "yes",
        "add_tables": "yes"
    }

@pytest.fixture
def complete_user_choices():
    return {
        "language": "fr",
        "detail_level": "detailed",
        "summary_type": "insights",
        "style": "bullet",
        "add_emojis": "no",
        "add_tables": "no",
        "specific_instructions": "Focus on key lessons."
    }

@pytest.fixture
def edge_case_user_choices():
    return {
        "language": "es",
        "detail_level": "short",
        "summary_type": "tools",
        "style": "text",
        "add_emojis": "no",
        "add_tables": "yes",
    }

@pytest.fixture
def invalid_user_choices():
    return {
        "language": "zz",  # Invalid language
        "detail_level": "unknown",  # Invalid detail level
        "summary_type": "invalid",  # Invalid summary type
        "style": "unknown",  # Invalid style
    }

# Tests pour build_common_instructions
def test_build_common_instructions_minimal(minimal_user_choices):
    instructions = build_common_instructions(minimal_user_choices)
    assert "Language: en" in instructions
    assert "Between 800 and 1000 words" in instructions
    assert "Provide a full summary" in instructions
    assert "Mix text and bullet points" in instructions
    assert "Absolutely add emojis" in instructions
    assert "ALWAYS Use markdown tables" in instructions
    assert "Additional instructions" not in instructions

def test_build_common_instructions_complete(complete_user_choices):
    instructions = build_common_instructions(complete_user_choices)
    assert "Language: fr" in instructions
    assert "Level of detail: Provide an extremely detailed summary" in instructions
    assert "Focus only on key insights" in instructions
    assert "Use ALWAYS AND ONLY bullet points" in instructions
    assert "Do not use emojis" in instructions
    assert "Do not use tables" in instructions
    assert "Additional instructions: Focus on key lessons" in instructions

def test_build_common_instructions_short_detail(edge_case_user_choices):
    instructions = build_common_instructions(edge_case_user_choices)
    assert "Language: es" in instructions
    assert "300 words maximum" in instructions
    assert "Extract all tools, methods, techniques" in instructions
    assert "Use ALWAYS AND ONLY plain text" in instructions
    assert "Do not use emojis" in instructions
    assert "ALWAYS Use markdown tables" in instructions

def test_build_common_instructions_invalid_options(invalid_user_choices):
    instructions = build_common_instructions(invalid_user_choices)
    assert "Language: zz" in instructions
    assert "As detailed as needed" in instructions  # Fallback for invalid detail level
    assert "Provide a full summary" in instructions  # Fallback for invalid summary type
    assert "Mix text and bullet points" in instructions  # Fallback for invalid style

# Tests pour build_final_prompt
def test_build_final_prompt(minimal_user_choices):
    fake_transcript = "This is a test transcript"
    prompt = build_final_prompt(fake_transcript, minimal_user_choices)
    assert BASE_PROMPT in prompt
    assert "Transcript:\nThis is a test transcript" in prompt
    assert "Language: en" in prompt

def test_build_final_prompt_empty_transcript(minimal_user_choices):
    prompt = build_final_prompt("", minimal_user_choices)
    assert BASE_PROMPT in prompt
    assert "Transcript:\n" in prompt
    assert len(prompt) > len(BASE_PROMPT)  # Assurez-vous que le prompt contient plus que juste le prompt de base

def test_build_final_prompt_with_logger(minimal_user_choices):
    with patch('services.prompt_builder.logger') as mock_logger:
        fake_transcript = "Test transcript"
        prompt = build_final_prompt(fake_transcript, minimal_user_choices)
        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0][0]
        assert "📦 Final prompt" in call_args
        assert prompt.strip() == prompt

# Tests pour build_initial_prompt
def test_build_initial_prompt(minimal_user_choices):
    fake_chunk = "This is chunk 1"
    prompt = build_initial_prompt(fake_chunk, minimal_user_choices)
    assert BASE_PROMPT in prompt
    assert "You will receive a long transcript split into several parts" in prompt
    assert "Transcript Part 1:" in prompt
    assert "This is chunk 1" in prompt
    assert "Language: en" in prompt

def test_build_initial_prompt_with_logger(minimal_user_choices):
    with patch('services.prompt_builder.logger') as mock_logger:
        fake_chunk = "This is chunk 1"
        prompt = build_initial_prompt(fake_chunk, minimal_user_choices)
        mock_logger.debug.assert_called_once_with("📥 Initial prompt created with chunk 1")

# Tests pour build_update_prompt
def test_build_update_prompt(minimal_user_choices):
    fake_chunk = "This is chunk 2"
    prev_summary = "Previous summary"
    chunk_id = 2
    
    prompt = build_update_prompt(fake_chunk, prev_summary, chunk_id, minimal_user_choices)
    assert "You are continuing a summarization task" in prompt
    assert "Previous summary" in prompt
    assert "Now integrate this new transcript part (Part 2)" in prompt
    assert "This is chunk 2" in prompt
    assert BASE_PROMPT in prompt
    assert "Language: en" in prompt

def test_build_update_prompt_with_larger_chunk_id(minimal_user_choices):
    fake_chunk = "This is chunk 5"
    prev_summary = "Previous summary of chunks 1-4"
    chunk_id = 5
    
    prompt = build_update_prompt(fake_chunk, prev_summary, chunk_id, minimal_user_choices)
    assert "Part 5" in prompt
    assert "Previous summary of chunks 1-4" in prompt

def test_build_update_prompt_with_logger(minimal_user_choices):
    with patch('services.prompt_builder.logger') as mock_logger:
        fake_chunk = "This is chunk 3"
        prev_summary = "Previous summary"
        chunk_id = 3
        
        prompt = build_update_prompt(fake_chunk, prev_summary, chunk_id, minimal_user_choices)
        mock_logger.debug.assert_called_once_with("🔁 Update prompt built for chunk 3") 