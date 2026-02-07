"""
Configuration settings for the Todo AI Chatbot
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/todo_chatbot")

    # MCP settings
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8080")

    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    reload: bool = os.getenv("RELOAD", "true").lower() == "true"

    # Application settings
    app_name: str = "Todo AI Chatbot"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a global settings instance
settings = Settings()