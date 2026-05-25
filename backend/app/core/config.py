"""
Application configuration management.
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Oil & Gas M&A Valuation Platform"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Gemini AI (reads from environment variable, falls back to hardcoded value)
    GEMINI_API_KEY: str = "AIzaSyCctuqFULVRYTgl3AMRHD1CyItf_0muX1Q"
    
    # Alpha Vantage API (for real-time market data)
    ALPHA_VANTAGE_API_KEY: str = "421057MQ0P4ACM7T"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = ["csv", "xlsx"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
