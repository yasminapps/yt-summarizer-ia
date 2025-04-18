from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from utils.decorators import safe_exec, log_execution, timed
from utils.logger import get_logger
import os
from dotenv import load_dotenv

logger = get_logger()
load_dotenv()

@timed
@log_execution
@safe_exec
def get_llm_client(engine, api_url=None, api_key=None):
    """
    Retourne la fonction IA appropriée selon le choix utilisateur.
    - Si openai-user est sélectionné et clé + URL présentes → OpenAI (clé utilisateur)
    - Si openai-default est sélectionné → OpenAI avec clé du projet
    - Sinon, fallback Ollama
    """
    logger.info(f"🔄 Configuration du client LLM avec moteur: {engine}")
    
    if engine == "ollama":
        logger.info("✓ Utilisation du client Ollama local")
        return call_ollama_llm
    
    elif engine == "openai-user":
        # Vérifier mais ne pas logger la clé API
        if not api_key:
            logger.warning("⚠️ Aucune clé API fournie pour OpenAI-User")
        else:
            logger.info("✓ Clé API utilisateur fournie pour OpenAI")
            
        # Masquer la clé dans les logs
        if api_url:
            logger.info(f"✓ URL API personnalisée: {api_url}")
        
        # Retourner le client avec les paramètres
        return lambda prompt: call_openai_llm(prompt, api_key=api_key, api_base=api_url)
    
    else:  # openai-default
        # Utiliser la clé par défaut de l'environnement
        default_api_key = os.getenv("OPENAI_API_KEY")
        if not default_api_key:
            logger.warning("⚠️ Aucune clé API par défaut dans les variables d'environnement")
        else:
            logger.info("✓ Utilisation de la clé API OpenAI par défaut")
            
        # Retourner le client avec la clé par défaut
    return lambda prompt: call_openai_llm(prompt)