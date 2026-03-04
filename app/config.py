import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL: str = "llama-3.1-8b-instant"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash"

    OPENALEX_URL: str = "https://api.openalex.org"
    OPENALEX_EMAIL: str | None = os.getenv("OPENALEX_EMAIL")

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    DATABASE_URL: str = "sqlite+aiosqlite:///./research_engine.db"

    PDF_OUTPUT_DIR: str = "pdfs"
    JSON_OUTPUT_DIR: str = "reports"

    WEIGHT_SIMILARITY: float = 0.4
    WEIGHT_CITATION: float = 0.3
    WEIGHT_RECENCY: float = 0.2
    WEIGHT_NOVELTY: float = 0.1

    LOG_LEVEL: str = "INFO"

    BACKEND_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

os.makedirs(settings.PDF_OUTPUT_DIR, exist_ok=True)
os.makedirs(settings.JSON_OUTPUT_DIR, exist_ok=True)
