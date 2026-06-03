from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # APP
    APP_NAME: str = "AskDrip AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # SECURITY
    SECRET_KEY: str

     # NODE BACKEND
    DRIPZOID_API_URL: str = (
        "https://api.dripzoid.com"
    )

    # DATABASE
    DATABASE_URL: str

    # AI MODEL
    MODEL_NAME: str = (
        "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"
    )

    # AI GENERATION SETTINGS
    MAX_NEW_TOKENS: int = 60
    TEMPERATURE: float = 0.4
    TOP_P: float = 0.9
    HF_TOKEN: str | None = None

    # RAG SETTINGS
    TOP_K_RESULTS: int = 2

    # API SETTINGS
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # OPTIONAL LEGACY SUPPORT
    OLLAMA_BASE_URL: str | None = None

    # Pydantic Config
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()