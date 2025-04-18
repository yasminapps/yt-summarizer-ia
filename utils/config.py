from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List
from dotenv import load_dotenv

class Config(BaseSettings):
    # Infos générales
    APP_NAME: str = "YouTube IA Summarizer"
    DEBUG: bool = False

    # OpenAI
    OPENAI_API_URL: str = "https://api.openai.com/v1/chat/completions"
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_ENCODING_MODEL: str = "gpt-3.5-turbo"

    # Résumé par défaut
    DEFAULT_LANGUAGE: str = "fr"
    DEFAULT_DETAIL_LEVEL: str = "medium"
    DEFAULT_SUMMARY_TYPE: str = "full"

    # Sécurité
    MAX_TOKENS: int = 10000
    ALLOWED_ENGINES: List[str] = ["openai-default", "openai-user", "ollama"]

    # Configuration de pydantic
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

def get_config():
    load_dotenv()
    return Config()

config = get_config()
       