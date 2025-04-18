# utils/logger.py
import logging
import os
from typing import Optional, Dict, Any, Union

# Définit le type Logger pour la documentation et le typage
Logger = logging.Logger

def get_logger(
    name: str = "yt-summarizer", 
    log_level: Union[int, str] = logging.DEBUG,
    log_to_file: bool = True,
    log_file_path: str = "logs/app.log",
    log_to_console: bool = True
) -> Logger:
    """
    Crée et configure un logger avec les paramètres spécifiés.
    
    Args:
        name: Nom du logger
        log_level: Niveau de logging (DEBUG, INFO, etc.)
        log_to_file: Si True, ajoute un FileHandler
        log_file_path: Chemin du fichier de log
        log_to_console: Si True, ajoute un ConsoleHandler
        
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    
    # Convertir log_level si c'est une chaîne
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper())
    
    logger.setLevel(log_level)

    # N'ajoute les handlers que s'ils n'existent pas déjà
    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        # Console handler
        if log_to_console:
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        # Fichier handler
        if log_to_file:
            log_dir = os.path.dirname(log_file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            fh = logging.FileHandler(log_file_path, encoding="utf-8")
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger
