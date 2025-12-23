"""
Configuration management for the Patient Education API
"""
import os
from typing import List
from functools import lru_cache

class Settings:
    """Application settings"""
    
    # App Info
    APP_TITLE: str = "Patient Education API"
    APP_VERSION: str = "3.0.0"
    
    # Google APIs
    SCOPES_DRIVE: List[str] = ['https://www.googleapis.com/auth/drive.readonly']
    SCOPES_SHEETS: List[str] = ['https://www.googleapis.com/auth/spreadsheets']
    
    # Google IDs
    MAIN_FOLDER_ID: str = os.getenv("MAIN_FOLDER_ID", "1f3yc3sQpnMVHHxFO8fK5SQlCj1-gN3jF")
    GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "1UAXXlBbDZwtUuqIkRWv7rNGSmy69vLKFB65w54A1J2c")
    GOOGLE_CREDENTIALS_JSON: str = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
    
    # Cache
    VIDEO_CACHE_DURATION: int = int(os.getenv("VIDEO_CACHE_DURATION", "1800"))  # 30 minutes
    
    # Disease folders mapping
    DISEASE_FOLDERS = {
        "diabetes": "Diabetes Mellitus",
        "hypertension": "Hypertension",
        "cardiac": "Heart disease"
    }
    
    # Server
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
