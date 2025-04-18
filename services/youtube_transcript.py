from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs
from utils.decorators import safe_exec, log_execution, timed
from utils.dependency_injector import inject_dependencies, inject_logger
from utils.logger import Logger
from utils.config import Config

@timed
@log_execution
@safe_exec
@inject_logger
def extract_video_id(youtube_url, logger=None):
    """
    Extrait l'ID d'une vidéo YouTube à partir de son URL.
    
    Args:
        youtube_url: L'URL de la vidéo YouTube
        logger: Instance de logger injectée
        
    Returns:
        str: L'ID de la vidéo, ou None si l'URL est invalide
    """
    try:
        parsed_url = urlparse(youtube_url)
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]
            logger.debug(f"🔍 ID vidéo extrait de l'URL youtube.com: {video_id}")
            return video_id
        elif parsed_url.hostname == "youtu.be":
            video_id = parsed_url.path.lstrip('/')
            logger.debug(f"🔍 ID vidéo extrait de l'URL youtu.be: {video_id}")
            return video_id
        else:
            logger.warning(f"⚠️ URL non reconnue comme une URL YouTube: {youtube_url}")
            return None
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'extraction de l'ID vidéo: {str(e)}")
        return None

@timed
@log_execution
@safe_exec
@inject_dependencies
def get_transcript_text(video_url, languages=None, logger=None, config=None):
    """
    Récupère le texte de la transcription d'une vidéo YouTube.
    
    Args:
        video_url: L'URL de la vidéo YouTube
        languages: Liste des langues à essayer (défaut: ['fr', 'en'])
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        str: Le texte de la transcription
        
    Raises:
        ValueError: Si l'URL est invalide ou la transcription n'est pas disponible
    """
    languages = languages or ['fr', 'en']
    logger.info(f"🎬 Récupération de la transcription pour {video_url}")
    
    video_id = extract_video_id(video_url, logger=logger)
    if not video_id:
        logger.error(f"❌ Lien YouTube invalide: {video_url}")
        raise ValueError("Lien YouTube invalide.")

    try:
        logger.debug(f"📝 Tentative avec les langues: {', '.join(languages)}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        
        # Formatage du texte
        text = "\n".join([entry['text'] for entry in transcript])
        logger.info(f"✅ Transcription récupérée avec succès ({len(text)} caractères)")
        
        return text
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération de la transcription: {str(e)}")
        raise ValueError(f"Erreur lors de la récupération de la transcription: {str(e)}")
