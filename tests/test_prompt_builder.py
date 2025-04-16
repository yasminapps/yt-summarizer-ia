import pytest
from services.prompt_builder import (
    build_common_instructions, 
    build_final_prompt, 
    build_initial_prompt, 
    build_update_prompt,
    BASE_PROMPT
)
from unittest.mock import patch

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
    assert "As detailed as needed" in instructions
    assert "Focus only on key insights" in instructions
    assert "Use ALWAYS AND ONLY bullet points" in instructions
    assert "Do not use emojis" in instructions
    assert "Do not use tables" in instructions
    assert "Additional instructions: Focus on key lessons" in instructions

# Tests pour build_final_prompt
def test_build_final_prompt(minimal_user_choices):
    fake_transcript = "This is a test transcript"
    prompt = build_final_prompt(fake_transcript, minimal_user_choices)
    assert BASE_PROMPT in prompt
    assert "Transcript:\nThis is a test transcript" in prompt
    assert "Language: en" in prompt

# Tests pour build_initial_prompt
def test_build_initial_prompt(minimal_user_choices):
    fake_chunk = "This is chunk 1"
    prompt = build_initial_prompt(fake_chunk, minimal_user_choices)
    assert BASE_PROMPT in prompt
    assert "You will receive a long transcript split into several parts" in prompt
    assert "Transcript Part 1:" in prompt
    assert "This is chunk 1" in prompt
    assert "Language: en" in prompt

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