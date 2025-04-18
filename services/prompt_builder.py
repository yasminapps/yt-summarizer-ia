from pathlib import Path
from utils.logger import Logger
from utils.config import Config
from utils.dependency_injector import inject_dependencies, inject_logger

# On chargera le prompt au moment de l'appel des fonctions
BASE_PROMPT_PATH = "prompts/prompt_yt_summary.md"
BASE_PROMPT = None  # Sera chargé dynamiquement

@inject_dependencies
def load_base_prompt(logger=None, config=None):
    """
    Charge le template de prompt depuis le fichier.
    Cette fonction est appelée automatiquement par les constructeurs de prompts.
    
    Args:
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        str: Le contenu du template de prompt
    """
    global BASE_PROMPT
    
    if BASE_PROMPT is not None:
        return BASE_PROMPT
        
    try:
        prompt_path = config.PROMPT_TEMPLATE_PATH if hasattr(config, 'PROMPT_TEMPLATE_PATH') else BASE_PROMPT_PATH
        BASE_PROMPT = Path(prompt_path).read_text()
        logger.info(f"✅ Base prompt template loaded from {prompt_path}")
        return BASE_PROMPT
    except Exception as e:
        logger.error(f"❌ Failed to load base prompt template: {e}")
        BASE_PROMPT = "You are an AI assistant that summarizes YouTube videos based on their transcripts."
        return BASE_PROMPT

@inject_logger
def build_common_instructions(user_choices: dict, logger=None) -> str:
    """
    Construit les instructions communes pour tous les types de prompts.
    
    Args:
        user_choices: Dictionnaire des choix utilisateur
        logger: Instance de logger injectée
        
    Returns:
        str: Les instructions formatées pour le prompt
    """
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

    logger.debug(f"🛠️ Construction des instructions avec les choix: {user_choices}")

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

@inject_dependencies
def build_final_prompt(transcript: str, user_choices: dict, logger=None, config=None) -> str:
    """
    Assemble le prompt complet (1 bloc unique).
    Utilise build_common_instructions() pour homogénéité.
    
    Args:
        transcript: Texte de la transcription
        user_choices: Dictionnaire des choix utilisateur
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        str: Le prompt complet
    """
    base_prompt = load_base_prompt(logger=logger, config=config)
    instructions = build_common_instructions(user_choices, logger=logger)

    final_prompt = f"{base_prompt}\n\nTranscript:\n{transcript}\n\n{instructions}"
    logger.debug(f"📦 Final prompt (single block):\n{final_prompt[:500]}...")
    return final_prompt.strip()

@inject_dependencies
def build_initial_prompt(transcript_chunk: str, user_choices: dict, logger=None, config=None) -> str:
    """
    Crée le prompt pour le premier chunk de transcript.
    Utilise les instructions dynamiques communes.
    
    Args:
        transcript_chunk: Premier morceau de la transcription
        user_choices: Dictionnaire des choix utilisateur
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        str: Le prompt initial
    """
    base_prompt = load_base_prompt(logger=logger, config=config)
    instructions = build_common_instructions(user_choices, logger=logger)

    prompt = f"""\
    {base_prompt}

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

@inject_dependencies
def build_update_prompt(transcript_chunk: str, prev_summary: str, chunk_id: int, user_choices: dict, logger=None, config=None) -> str:
    """
    Crée le prompt pour les chunks suivants.
    Le résumé précédent est transmis pour mise à jour.
    
    Args:
        transcript_chunk: Morceau de transcription actuel
        prev_summary: Résumé précédent
        chunk_id: Numéro du chunk actuel
        user_choices: Dictionnaire des choix utilisateur
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        str: Le prompt de mise à jour
    """ 
    base_prompt = load_base_prompt(logger=logger, config=config)
    instructions = build_common_instructions(user_choices, logger=logger)

    prompt = f"""
You are continuing a summarization task.

Here is the previous summary based on the previous parts:
{prev_summary}

Now integrate this new transcript part (Part {chunk_id}) into the existing summary:
{transcript_chunk}

Update and expand the summary, keeping consistency and structure.
{base_prompt}
{instructions}
""".strip()

    logger.debug(f"🔁 Update prompt built for chunk {chunk_id}")
    return prompt