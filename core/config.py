from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Project Configuration
    PROJECT_NAME: str = "Feedback API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "dev"  # dev/staging/prod

    # API Configuration
    API_PREFIX: str = "/api/v1"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"

    # Security Configuration
    CORS_ORIGINS: List[str] = ["*"]  # Restrict in prod
    API_KEY_HEADER: str = "X-API-Key"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # Database Configuration
    DB_TYPES: List[str]  # Example: ["mongodb", "postgres"]
    DB_URIS: List[str]   # Example: ["mongodb://localhost:27017", "postgresql://user:pass@localhost/db"]
    DB_NAMES: List[str]  # Example: ["feedback_db", "feedback_api"] (needed for MongoDB)
    
    # Port Value
    PORT: int

    # Pydantic v2+ configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
