"""Settings with proper environment variable handling."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # LLM Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    llm_model: str = Field(default="gpt-4o-mini", description="LLM model")
    
    # Vector Database
    qdrant_host: str = Field(default="localhost", description="Qdrant host")
    qdrant_port: int = Field(default=6333, description="Qdrant port")
    vector_db_path: str = Field(default="./data/vector_db", description="Vector DB path")
    
    # CRM Configuration
    crm_api_url: str = Field(default="https://api.example-crm.com", description="CRM API URL")
    crm_api_key: str = Field(default="", description="CRM API key")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379", description="Redis URL")

# Global settings instance
settings = Settings()