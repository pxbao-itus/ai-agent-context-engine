from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Context Engine RAG"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    
    # Postgres
    POSTGRES_DSN: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION_NAME: str = "us-east-1"
    S3_BUCKET_NAME: str = "my-rag-bucket"
    S3_ENDPOINT_URL: str | None = None
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # options: openai, anthropic, google
    LOG_STORAGE_PROVIDER: str = "postgres"  # options: postgres
    
    # Anthropic
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-haiku-20240307"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Google (Gemini)
    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-2.0-flash"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
