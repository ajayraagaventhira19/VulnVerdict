from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "examate-rag"
    environment: str = "local"

    gemini_api_key: SecretStr = SecretStr("")
    gemini_primary_model: str = "gemini-3.5-flash"
    gemini_fallback_model: str = "gemini-3.7-flash"


@lru_cache
def get_settings() -> Settings:
    return Settings()
