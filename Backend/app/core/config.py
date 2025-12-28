from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = Field(default="dev")
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_DB: str | None = None
    DATABASE_URL_ASYNC: str | None = None
    DATABASE_URL_SYNC: str | None = None
    JWT_SECRET_KEY: str = "test-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEBUG: bool = False


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

