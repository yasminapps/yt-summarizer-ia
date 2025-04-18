from services.ollama_client import call_ollama_llm
from services.openai_client import call_openai_llm
from utils.decorators import safe_exec, log_execution, timed
from utils.dependency_injector import inject_dependencies
from utils.logger import Logger
from utils.config import Config
import os
from dotenv import load_dotenv

load_dotenv()

@timed
@log_execution
@safe_exec
@inject_dependencies
def get_llm_client(
    engine: str, 
    api_url: str = None, 
    api_key: str = None,
    logger: Logger = None,
    config: Config = None
):
    """
    Retourne la fonction IA appropriée selon le choix utilisateur.
    
    Args:
        engine: Moteur IA à utiliser (ollama, openai-user, openai-default)
        api_url: URL de l'API (pour openai-user)
        api_key: Clé API (pour openai-user)
        logger: Instance de logger injectée
        config: Instance de configuration injectée
        
    Returns:
        Callable: Fonction qui prend un prompt et retourne une réponse
    """
    logger.info(f"🔄 Configuration du client LLM avec moteur: {engine}")
    
    # Vérifier que le moteur est autorisé
    if engine not in config.ALLOWED_ENGINES:
        logger.warning(f"⚠️ Moteur {engine} non reconnu, utilisation du moteur par défaut")
        engine = "openai-default"
    
    if engine == "ollama":
        logger.info("✓ Utilisation du client Ollama local")
        return lambda prompt: call_ollama_llm(prompt, logger=logger, config=config)
    
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
        return lambda prompt: call_openai_llm(
            prompt, 
            api_key=api_key, 
            api_url=api_url,
            model=config.OPENAI_MODEL,
            logger=logger,
            config=config
        )
    
    else:  # openai-default
        # Utiliser la clé par défaut de l'environnement
        default_api_key = os.getenv("OPENAI_API_KEY")
        if not default_api_key:
            logger.warning("⚠️ Aucune clé API par défaut dans les variables d'environnement")
        else:
            logger.info("✓ Utilisation de la clé API OpenAI par défaut")
            
        # Retourner le client avec la clé par défaut et les dépendances injectées
        return lambda prompt: call_openai_llm(
            prompt,
            model=config.OPENAI_MODEL,
            logger=logger,
            config=config
        )