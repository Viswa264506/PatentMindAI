from pydantic_settings import BaseSettings, SettingsConfigDict
import logging


class Settings(BaseSettings):
    """
    Central application settings.
    Values are automatically loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # -----------------------------
    # Groq Configuration
    # -----------------------------
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    # -----------------------------
    # Patent APIs
    # -----------------------------
    LENS_API_KEY: str = ""
    USPTO_API_KEY: str = ""

    # -----------------------------
    # Application
    # -----------------------------
    APP_NAME: str = "PatentMind AI"
    LOG_LEVEL: str = "INFO"
    REQUEST_TIMEOUT: int = 10

    # -----------------------------
    # PostgreSQL
    # -----------------------------
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "patentmind"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""


settings = Settings()


# -----------------------------
# Logging
# -----------------------------
def setup_logging():

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    return logging.getLogger(settings.APP_NAME)


logger = setup_logging()