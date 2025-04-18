"""
Module pour gérer l'injection de dépendances dans l'application.
Ce module centralise l'accès aux services et configurations pour faciliter
les tests et réduire le couplage.
"""
from typing import Optional, Dict, Any, Callable
from utils.config import Config, get_config
from utils.logger import get_logger, Logger

class DependencyContainer:
    """
    Conteneur de dépendances pour l'application.
    Centralise l'accès aux services, configurations et utilitaires.
    """
    def __init__(self):
        self._config = None
        self._logger = None
        self._services = {}
        
    @property
    def config(self) -> Config:
        """Retourne l'instance de configuration, l'initialise si nécessaire"""
        if self._config is None:
            self._config = get_config()
        return self._config
    
    @config.setter
    def config(self, config: Config) -> None:
        """Permet de remplacer la configuration par une instance personnalisée"""
        self._config = config
    
    @property
    def logger(self) -> Logger:
        """Retourne l'instance de logger, l'initialise si nécessaire"""
        if self._logger is None:
            self._logger = get_logger()
        return self._logger
    
    @logger.setter
    def logger(self, logger: Logger) -> None:
        """Permet de remplacer le logger par une instance personnalisée"""
        self._logger = logger
    
    def register_service(self, name: str, service: Any) -> None:
        """Enregistre un service dans le conteneur"""
        self._services[name] = service
    
    def get_service(self, name: str) -> Any:
        """Récupère un service du conteneur"""
        if name not in self._services:
            raise KeyError(f"Service '{name}' non enregistré dans le conteneur")
        return self._services[name]
    
    def has_service(self, name: str) -> bool:
        """Vérifie si un service est enregistré"""
        return name in self._services

# Instance globale du conteneur de dépendances
container = DependencyContainer()

# Fonctions utilitaires pour simplifier l'injection de dépendances
def get_container() -> DependencyContainer:
    """Retourne l'instance du conteneur de dépendances"""
    return container

def inject_config(func: Callable) -> Callable:
    """
    Décorateur pour injecter automatiquement la configuration
    """
    def wrapper(*args, config=None, **kwargs):
        config = config or container.config
        return func(*args, config=config, **kwargs)
    return wrapper

def inject_logger(func: Callable) -> Callable:
    """
    Décorateur pour injecter automatiquement le logger
    """
    def wrapper(*args, logger=None, **kwargs):
        logger = logger or container.logger
        return func(*args, logger=logger, **kwargs)
    return wrapper

def inject_dependencies(func: Callable) -> Callable:
    """
    Décorateur pour injecter automatiquement toutes les dépendances
    """
    def wrapper(*args, config=None, logger=None, **kwargs):
        config = config or container.config
        logger = logger or container.logger
        return func(*args, config=config, logger=logger, **kwargs)
    return wrapper 