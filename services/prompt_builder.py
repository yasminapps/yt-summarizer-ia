from pathlib import Path
from utils.logger import get_logger
from utils.config import Config
from utils.dependency_injector import inject_dependencies, inject_logger

# On chargera le prompt au moment de l'appel des fonctions
BASE_PROMPT_PATH = "prompts/prompt_yt_summary.md"
BASE_PROMPT = None  # Sera chargé dynamiquement

@inject_dependencies
def load_base_prompt(logger=None, config=None):
    """Charge le template de prompt à partir du fichier de configuration.
    
    Lit le fichier de template de prompt et le met en cache pour éviter de relire
    le fichier à chaque appel. Utilise la configuration pour déterminer le chemin
    du fichier, avec une valeur par défaut.
    
    Args:
        logger: Instance de logger pour journalisation
        config: Instance de configuration
        
    Returns:
        str: Le contenu du template de prompt
    """
    global BASE_PROMPT
    
    # Vérifier si un chemin personnalisé est fourni dans la configuration
    prompt_path = getattr(config, 'PROMPT_TEMPLATE_PATH', BASE_PROMPT_PATH)
    
    # Si BASE_PROMPT est déjà chargé et qu'on utilise le chemin par défaut, on le réutilise
    if BASE_PROMPT is not None and prompt_path == BASE_PROMPT_PATH:
        return BASE_PROMPT
        
    try:
        BASE_PROMPT = Path(prompt_path).read_text()
        logger.info(f"✅ Base prompt template loaded from {prompt_path}")
        return BASE_PROMPT
    except Exception as e:
        logger.error(f"❌ Failed to load base prompt template: {e}")
        fallback_prompt = "You are an AI assistant that summarizes YouTube videos based on their transcripts."
        BASE_PROMPT = fallback_prompt
        return fallback_prompt

@inject_dependencies
def build_common_instructions(user_choices: dict, logger=None, config=None) -> str:
    """Construit les instructions communes pour tous les types de prompts.
    
    Génère un bloc d'instructions formaté en Markdown qui sera ajouté à tous
    les prompts, en fonction des choix utilisateur (langue, niveau de détail, etc.)
    
    Args:
        user_choices: Dictionnaire des choix utilisateur contenant:
            language: Langue du résumé (fr, en, etc.)
            detail_level: Niveau de détail (short, medium, detailed)
            summary_type: Type de résumé (full, tools, insights)
            style: Style de présentation (bullet, text, mixed)
            add_emojis: Ajouter des emojis (yes, no)
            add_tables: Ajouter des tableaux (yes, no)
            specific_instructions: Instructions spécifiques supplémentaires
        
    Returns:
        Texte formaté contenant les instructions pour le prompt
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
    """Assemble le prompt complet en un seul bloc.
    
    Crée un prompt complet pour générer un résumé en une seule fois,
    sans découpage en morceaux. Combine le prompt de base, la transcription
    complète et les instructions personnalisées.
    
    Args:
        transcript: Texte complet de la transcription à résumer
        user_choices: Dictionnaire des choix utilisateur pour la personnalisation
        
    Returns:
        Prompt complet formaté prêt à être envoyé à l'IA
    """
    base_prompt = load_base_prompt(logger=logger, config=config)
    instructions = build_common_instructions(user_choices, logger=logger, config=config)

    final_prompt = f"{base_prompt}\n\nTranscript:\n{transcript}\n\n{instructions}"
    # Pour compatibilité avec les tests existants
    logger.debug("📦 Final prompt (single block):\n" + base_prompt + "\n\nTranscript:\n" + transcript + "\n\n...")
    return final_prompt.strip()

@inject_dependencies
def build_initial_prompt(transcript_chunk: str, user_choices: dict, logger=None, config=None) -> str:
    """Crée le prompt pour le premier segment de transcription.
    
    Construit un prompt spécial pour le premier segment lorsque la transcription
    est traitée en plusieurs parties. Inclut des instructions spécifiques sur
    comment commencer le processus de résumé séquentiel.
    
    Args:
        transcript_chunk: Premier segment de la transcription
        user_choices: Dictionnaire des choix utilisateur pour la personnalisation
        
    Returns:
        Prompt initial formaté pour le premier segment
    """
    base_prompt = load_base_prompt(logger=logger, config=config)
    instructions = build_common_instructions(user_choices, logger=logger, config=config)

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
    
    logger.debug("📥 Initial prompt created with chunk 1")
    return prompt.strip()

@inject_dependencies
def build_update_prompt(transcript_chunk: str, prev_summary: str, chunk_id: int, user_choices: dict, logger=None, config=None) -> str:
    """Crée le prompt pour les segments suivants de la transcription.
    
    Construit un prompt pour mettre à jour et enrichir le résumé existant
    avec un nouveau segment de la transcription. Permet un traitement séquentiel
    des longues transcriptions tout en maintenant la cohérence.
    
    Args:
        transcript_chunk: Segment actuel de la transcription
        prev_summary: Résumé des segments précédents
        chunk_id: Numéro du segment actuel
        user_choices: Dictionnaire des choix utilisateur pour la personnalisation
        
    Returns:
        Prompt de mise à jour formaté pour le segment actuel
    """
    base_prompt = load_base_prompt(logger=logger, config=config)
    instructions = build_common_instructions(user_choices, logger=logger, config=config)

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