from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

def build_final_prompt(transcript: str, user_choices: dict) -> str:
    """
    Assemble le prompt complet avec :
    - prompt de base
    - transcript
    - instructions dynamiques (langue, niveau de détail, style, emojis, tableaux, specific instructions)
    """

    # Charger ton template .txt
    base_prompt = Path("prompts/prompt_yt_summary.md").read_text()

    # Définir les instructions dynamiques
    detail_mapping = {
        "short": "100 words maximum.",
        "medium": "Between 500 and 600 words.",
        "detailed": "As detailed as needed (more than 1000 words if necessary)."
    }

    summary_type_mapping = {
        "full": "Provide a full summary of the video.",
        "tools": "Extract all tools, methods, techniques, strategies, lists or actionable content mentioned in the video.",
        "insights": "Focus only on key insights or lessons."
    }

    style_mapping = {
        "bullet": "Use only bullet points.",
        "text": "Use only plain text",
        "mixed": "Mix text and bullet points."
    }

    instructions = f"""
### Specific instructions for this summary:

- Language: {user_choices['language']}
- Detail level: {detail_mapping.get(user_choices['detail_level'], 'As detailed as needed')}
- Type of summary: {summary_type_mapping.get(user_choices['summary_type'], 'Provide a full summary.')}

- Style: {style_mapping.get(user_choices['style'], 'Mix text and bullet points.')}

- Emojis: {"Add emojis when useful." if user_choices.get('add_emojis') == "yes" else "Do not use emojis, NEVER."}

- Tables: {"Use tables if relevant." if user_choices.get('add_tables') == "yes" else "Do not use tables, NEVER."}

"""

    if user_choices.get("specific_instructions"):
        instructions += f"\n- Additional instructions: {user_choices['specific_instructions']}\n"

    instructions += "\n- The entire summary must be written in Markdown format."

    # Construire le prompt final
    final_prompt = f"{base_prompt}\n\nTranscript:\n{transcript}\n\n{instructions}"

    logger.debug(f"Specific instructions sent to LLM:\n{instructions}")

    return final_prompt.strip()