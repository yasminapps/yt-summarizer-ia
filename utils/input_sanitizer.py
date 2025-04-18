"""
Module dédié à la sanitisation des entrées utilisateur pour éviter les injections et autres problèmes de sécurité.
"""
import re
import html
from typing import Dict, List, Any, Optional, Union

def sanitize_url(url: str) -> str:
    """
    Sanitise une URL pour éviter les injections.
    Ne conserve que les URL de YouTube valides.
    """
    url = url.strip()
    # Vérifie que c'est une URL YouTube valide
    youtube_pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}.*$'
    if not re.match(youtube_pattern, url):
        return ""
    
    # Échappe les caractères HTML pour éviter les XSS
    return html.escape(url)

def sanitize_language(language: str) -> str:
    """
    Sanitise le code de langue pour n'autoriser que les codes ISO valides.
    """
    language = language.strip().lower()
    # Liste non exhaustive des codes de langue ISO 639-1
    valid_languages = ['en', 'fr', 'es', 'de', 'it', 'pt', 'nl', 'ru', 'zh', 'ja', 'ko', 'ar']
    
    if language in valid_languages:
        return language
    return "en"  # Langue par défaut

def sanitize_engine_choice(engine: str, default: str = "ollama") -> str:
    """
    Sanitise le choix du moteur IA.
    Accepte un moteur par défaut en paramètre.
    """
    engine = engine.strip().lower()
    valid_engines = ['ollama', 'openai-user', 'openai-default']
    
    if engine in valid_engines:
        return engine
    return default  # Utilise le moteur par défaut fourni

def sanitize_detail_level(detail_level: str) -> str:
    """
    Sanitise le niveau de détail demandé.
    """
    detail_level = detail_level.strip().lower()
    valid_levels = ['short', 'medium', 'detailed']
    
    if detail_level in valid_levels:
        return detail_level
    return "medium"  # Niveau par défaut

def sanitize_summary_type(summary_type: str) -> str:
    """
    Sanitise le type de résumé demandé.
    """
    summary_type = summary_type.strip().lower()
    valid_types = ['full', 'tools', 'insights']
    
    if summary_type in valid_types:
        return summary_type
    return "full"  # Type par défaut

def sanitize_style(style: str) -> str:
    """
    Sanitise le style de résumé demandé.
    """
    style = style.strip().lower()
    valid_styles = ['bullet', 'text', 'mixed']
    
    if style in valid_styles:
        return style
    return "mixed"  # Style par défaut

def sanitize_boolean_choice(choice: str) -> str:
    """
    Sanitise les choix booléens (oui/non).
    """
    choice = choice.strip().lower()
    if choice in ['yes', 'true', '1', 'oui']:
        return "yes"
    return "no"

def sanitize_api_url(url: str) -> str:
    """
    Sanitise l'URL de l'API.
    """
    url = url.strip()
    # Vérifie que c'est une URL valide
    if not url:
        return ""
    
    # Pattern pour les URLs normales et localhost
    url_pattern = r'^https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|localhost)(:\d+)?(/.*)?$'
    if not re.match(url_pattern, url):
        return ""
    
    return html.escape(url)

def sanitize_text_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitise un texte général (instructions spécifiques, etc.).
    """
    if not text:
        return ""
    
    # Limiter la longueur
    text = text[:max_length]
    
    # Supprimer les caractères dangereux
    text = re.sub(r'[^\w\s.,;:!?()\[\]{}\-"\'`]', '', text)
    
    # Échappe les caractères HTML pour éviter les XSS
    return html.escape(text)

def sanitize_form_data(form_data: Dict[str, str]) -> Dict[str, str]:
    """
    Sanitise toutes les données de formulaire en une fois.
    """
    sanitized = {}
    
    # Sanitisation des champs connus
    if 'youtube_url' in form_data:
        sanitized['youtube_url'] = sanitize_url(form_data.get('youtube_url', ''))
    
    # Utiliser openai-default comme valeur par défaut pour engine
    if 'engine' in form_data:
        sanitized['engine'] = sanitize_engine_choice(form_data.get('engine', ''), default="openai-default")
    
    if 'language' in form_data:
        sanitized['language'] = sanitize_language(form_data.get('language', ''))
    
    if 'detail_level' in form_data:
        sanitized['detail_level'] = sanitize_detail_level(form_data.get('detail_level', ''))
    
    if 'summary_type' in form_data:
        sanitized['summary_type'] = sanitize_summary_type(form_data.get('summary_type', ''))
    
    if 'style' in form_data:
        sanitized['style'] = sanitize_style(form_data.get('style', ''))
    
    if 'add_emojis' in form_data:
        sanitized['add_emojis'] = sanitize_boolean_choice(form_data.get('add_emojis', ''))
    
    if 'add_tables' in form_data:
        sanitized['add_tables'] = sanitize_boolean_choice(form_data.get('add_tables', ''))
    
    if 'api_url' in form_data:
        sanitized['api_url'] = sanitize_api_url(form_data.get('api_url', ''))
    
    if 'api_key' in form_data:
        # On ne sanitise pas la clé API, on la garde telle quelle
        sanitized['api_key'] = form_data.get('api_key', '')
    
    if 'specific_instructions' in form_data:
        sanitized['specific_instructions'] = sanitize_text_input(form_data.get('specific_instructions', ''))
    
    return sanitized 