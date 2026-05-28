"""
Configuration module for AMK AI Coder Platform
Handles environment variables and security settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "AMK AI Coder Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",
    ]
    
    # Firebase (server-side)
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_PRIVATE_KEY: Optional[str] = None
    FIREBASE_CLIENT_EMAIL: Optional[str] = None
    
    # OpenRouter (default AI provider)
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"
    
    # Alternative AI Providers (fallback)
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Chat Settings
    MAX_CONTEXT_MESSAGES: int = 20
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


def get_firebase_credentials() -> Optional[dict]:
    """Get Firebase credentials for server-side verification"""
    if settings.FIREBASE_PROJECT_ID and settings.FIREBASE_PRIVATE_KEY and settings.FIREBASE_CLIENT_EMAIL:
        return {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
        }
    return None


def get_api_key_for_provider(provider: str) -> Optional[str]:
    """Get API key for a specific provider"""
    keys = {
        "openrouter": settings.OPENROUTER_API_KEY,
        "gemini": settings.GEMINI_API_KEY,
        "groq": settings.GROQ_API_KEY,
        "openai": settings.OPENAI_API_KEY,
        "claude": settings.CLAUDE_API_KEY,
    }
    return keys.get(provider.lower())


def is_configured() -> bool:
    """Check if the application is properly configured"""
    return bool(settings.OPENROUTER_API_KEY or settings.FIREBASE_PROJECT_ID)