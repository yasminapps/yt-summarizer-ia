"""
Module dédié à la sanitisation des entrées utilisateur pour éviter les injections et autres problèmes de sécurité.
"""
import re
import html
from typing import Dict, List, Any, Optional, Union
from utils.logger import get_logger
from utils.config import config
from urllib.parse import urlparse

logger = get_logger()

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
    if re.match(r'^[a-z]{2}$', language):
        return language
    return config.DEFAULT_LANGUAGE  # Langue par défaut depuis config

def sanitize_engine_choice(choice: str, default: str = "openai-default") -> str:
    """
    Sanitise le choix du moteur IA.
    Accepte un moteur par défaut en paramètre.
    """
    valid_choices = ["openai-default", "openai-user", "ollama"]
    return choice if choice in valid_choices else default

def sanitize_detail_level(detail_level: str) -> str:
    """
    Sanitise le niveau de détail demandé.
    """
    valid_levels = ["short", "medium", "detailed"]
    return detail_level if detail_level in valid_levels else config.DEFAULT_DETAIL_LEVEL

def sanitize_summary_type(summary_type: str) -> str:
    """
    Sanitise le type de résumé demandé.
    """
    valid_types = ["full", "tools", "insights"]
    return summary_type if summary_type in valid_types else config.DEFAULT_SUMMARY_TYPE

def sanitize_style(style: str) -> str:
    """
    Sanitise le style de résumé demandé.
    """
    valid_styles = ["mixed", "bullet_points", "text_only"]
    return style if style in valid_styles else "mixed"

def sanitize_boolean_choice(choice: str) -> str:
    """
    Sanitise les choix booléens (oui/non).
    """
    return "yes" if choice == "yes" else "no"

def sanitize_api_url(url: str) -> str:
    """
    Vérifie et nettoie une URL d'API. Retourne une chaîne vide si l'URL est invalide.
    """
    url = url.strip()
    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        return ""

    if not parsed.netloc or "." not in parsed.netloc or parsed.hostname.startswith(".") or parsed.hostname.endswith("."):
       # autorise localhost ou 127.0.0.1
        if parsed.hostname not in ["localhost", "127.0.0.1"]:
            return ""
    
    return url
def sanitize_text_input(text: str, max_length: int = 10000) -> str:
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
    Sanitise les données du formulaire pour éviter les injections
    et uniformise les valeurs
    """
    sanitized = {}
    
    # Nettoyage URL YouTube
    youtube_url = form_data.get("youtube_url", "")
    sanitized["youtube_url"] = sanitize_url(youtube_url)
    
    # Moteur d'IA (validation pour éviter des injections)
    engine = form_data.get("engine", "openai-default")
    sanitized["engine"] = sanitize_engine_choice(engine)
    
    # API Key (nettoyage et masquage dans les logs)
    api_key = form_data.get("api_key", "").strip()
    sanitized["api_key"] = api_key
    
    # Ne jamais logger la clé API complète
    if api_key:
        logger.debug(f"API Key fournie: {'*' * min(len(api_key), 5)}")
    
    # URL API (validation basique)
    api_url = form_data.get("api_url", "")
    sanitized["api_url"] = sanitize_api_url(api_url)
    
    # Type de résumé (validation)
    summary_type = form_data.get("summary_type", "full")
    sanitized["summary_type"] = sanitize_summary_type(summary_type)
    
    # Langue (validation)
    language = form_data.get("language", "en")
    sanitized["language"] = sanitize_language(language)
    
    # Niveau de détail (validation)
    detail_level = form_data.get("detail_level", "medium")
    sanitized["detail_level"] = sanitize_detail_level(detail_level)
    
    # Style (validation)
    style = form_data.get("style", "mixed")
    sanitized["style"] = sanitize_style(style)
    
    # Emojis (validation)
    add_emojis = form_data.get("add_emojis", "yes")
    sanitized["add_emojis"] = sanitize_boolean_choice(add_emojis)
    
    # Tables (validation)
    add_tables = form_data.get("add_tables", "yes")
    sanitized["add_tables"] = sanitize_boolean_choice(add_tables)
    
    # Instructions spécifiques (nettoyage)
    specific_instructions = form_data.get("specific_instructions", "")
    sanitized["specific_instructions"] = sanitize_text_input(specific_instructions)
    
    return sanitized 