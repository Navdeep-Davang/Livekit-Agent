from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError
from functools import lru_cache
import os
import sys

class Settings(BaseSettings):
    LIVEKIT_URL: str
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    SARVAM_API_KEY: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        # Search for .env in current directory and parent directory
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings():
    try:
        return Settings()
    except ValidationError as e:
        print("\n" + "="*50)
        print("CONFIGURATION ERROR")
        print("="*50)
        print("Missing or invalid environment variables detected:")
        for error in e.errors():
            print(f"  - {error['loc'][0]}: {error['msg']}")
        print("\nMake sure you have a .env file in the root or backend directory.")
        print("Use backend/env.example as a template.")
        print("="*50 + "\n")
        sys.exit(1)

settings = get_settings()
