from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

# Charger le template prompt une seule fois au démarrage du module
BASE_PROMPT_PATH = "prompts/prompt_yt_summary.md"
try:
    BASE_PROMPT = Path(BASE_PROMPT_PATH).read_text()
    logger.info(f"✅ Base prompt template loaded from {BASE_PROMPT_PATH}")
except Exception as e:
    logger.error(f"❌ Failed to load base prompt template: {e}")
    BASE_PROMPT = "You are an AI assistant that summarizes YouTube videos based on their transcripts."

def build_common_instructions(user_choices: dict) -> str:
    detail_mapping = {
        "short": "300 words maximum.",
        "medium": "Between 800 and 1000 words.",
        "detailed": "Level of detail: Provide an extremely detailed summary. Cover each important concept, method, or insight thoroughly. Include examples, figures, and context when mentioned. Write as if the reader had no access to the video but needs to fully understand the content. Target length: Aim for more than 1500 words."
    }

    summary_type_mapping = {
        "full": "Provide a full summary of the video.",
        "tools": "Extract all tools, methods, techniques, strategies, lists or actionable content mentioned in the video.",
        "insights": "Focus only on key insights or lessons."
    }

    style_mapping = {
        "bullet": "Use ALWAYS AND ONLY bullet points. NO PLAIN TEXT.",
        "text": "Use ALWAYS AND ONLY plain text. NO BULLET POINTS.",
        "mixed": "Mix text and bullet points."
    }

    instructions = f"""
### Specific instructions for this summary:

- Language: {user_choices['language']}
- Detail level: {detail_mapping.get(user_choices['detail_level'], 'As detailed as needed')}
- Type of summary: {summary_type_mapping.get(user_choices['summary_type'], 'Provide a full summary.')}

- Style: {style_mapping.get(user_choices['style'], 'Mix text and bullet points.')}

- Emojis: {"Absolutely add emojis in the summary, ALWAYS." if user_choices.get('add_emojis') == "yes" else "Do not use emojis, NEVER."}

- Tables: {"ALWAYS Use markdown tables at least once, twice or more if needed." if user_choices.get('add_tables') == "yes" else "Do not use tables, NEVER."}
"""

    if user_choices.get("specific_instructions"):
        instructions += f"\n- Additional instructions: {user_choices['specific_instructions']}"

    instructions += "\n- The entire summary must be written in Markdown format."
    return instructions.strip()

def build_final_prompt(transcript: str, user_choices: dict) -> str:
    """
    Assemble le prompt complet (1 bloc unique).
    Utilise build_common_instructions() pour homogénéité.
    """
    instructions = build_common_instructions(user_choices)

    final_prompt = f"{BASE_PROMPT}\n\nTranscript:\n{transcript}\n\n{instructions}"
    logger.debug(f"📦 Final prompt (single block):\n{final_prompt[:500]}...")
    return final_prompt.strip()

def build_initial_prompt(transcript_chunk: str, user_choices: dict) -> str:
    """
    Crée le prompt pour le premier chunk de transcript.
    Utilise les instructions dynamiques communes.
    """
    instructions = build_common_instructions(user_choices)

    prompt = f"""\
    {BASE_PROMPT}

    You will receive a long transcript split into several parts. Your task is to summarize them sequentially.
    Start by summarizing the first part only.
    Then, for each new part, update and enrich your previous summary by integrating the new information.
    Ensure the result remains coherent, structured, and meaningful as a whole.
    Avoid repeating what has already been summarized.
    At the end, the final summary should feel like a single, unified piece of writing, not a sequence of fragments.

    Transcript Part 1:
    {transcript_chunk}

    {instructions}
    """
    logger.debug(f"📥 Initial prompt created with chunk 1")
    return prompt.strip()

def build_update_prompt(transcript_chunk: str, prev_summary: str, chunk_id: int, user_choices: dict) -> str:
    """
    Crée le prompt pour les chunks suivants.
    Le résumé précédent est transmis pour mise à jour.
    """ 
    instructions = build_common_instructions(user_choices)

    prompt = f"""
You are continuing a summarization task.

Here is the previous summary based on the previous parts:
{prev_summary}

Now integrate this new transcript part (Part {chunk_id}) into the existing summary:
{transcript_chunk}

Update and expand the summary, keeping consistency and structure.
{BASE_PROMPT}
{instructions}
""".strip()

    logger.debug(f"🔁 Update prompt built for chunk {chunk_id}")
    return prompt