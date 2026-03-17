from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./bank.db"
    app_env: str = "development"
    app_title: str = "Bank API"
    app_version: str = "1.0.0"
    secret_key: str = "dev-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    allowed_origins: str = "http://localhost:3000"

    @property
    def origins_list(self): return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]
    @property
    def is_production(self): return self.app_env == "production"
    @property
    def is_postgres(self): return "postgresql" in self.database_url
    @property
    def is_sqlite(self): return "sqlite" in self.database_url

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

@lru_cache
def get_settings(): return Settings()
