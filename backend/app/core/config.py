from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'Cachipilapp API'
    app_env: str = 'development'
    database_url: str = 'postgresql+psycopg2://app:app@localhost:5432/whatsapp_commerce'
    cors_origins: str = 'http://localhost:5173'

    @field_validator('database_url')
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Ensure credentials are URL-encoded for DB drivers expecting UTF-8 DSNs."""
        return make_url(value).render_as_string(hide_password=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
