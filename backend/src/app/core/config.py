import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Marketing Tool"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"  # JWT algorithm
    
    # POSTGRESQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "")
    
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    @property
    def get_database_uri(self) -> str:
        """Construct database URI from components."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}?sslmode=require"
    
    # EXTERNAL APIS
    HUGGINGFACE_TOKEN: Optional[str] = os.getenv("HUGGINGFACE_TOKEN", "")

    # SOCIAL MEDIA API KEYS
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    FACEBOOK_APP_ID: str = os.getenv("FACEBOOK_APP_ID", "")
    FACEBOOK_APP_SECRET: str = os.getenv("FACEBOOK_APP_SECRET", "")
    LINKEDIN_CLIENT_ID: str = os.getenv("LINKEDIN_CLIENT_ID", "")
    LINKEDIN_CLIENT_SECRET: str = os.getenv("LINKEDIN_CLIENT_SECRET", "")

    # MODEL SETTINGS
    MODEL_DIR: str = os.getenv("MODEL_DIR", os.path.join(os.getcwd(), "models"))
    TRAINED_MODEL_PATH: Optional[str] = os.getenv("TRAINED_MODEL_PATH", None)

    # Google Cloud / Dialogflow Configuration
    GOOGLE_CLOUD_PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "ai-marketing-chatbot-460708")
    if not GOOGLE_CLOUD_PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None)
    DIALOGFLOW_LANGUAGE_CODE: str = os.getenv("DIALOGFLOW_LANGUAGE_CODE", "en-US")
    
    # Chatbot Configuration
    CHATBOT_SESSION_TIMEOUT: int = os.getenv("CHATBOT_SESSION_TIMEOUT", 1800)  # 30 minutes
    CHATBOT_MAX_MESSAGE_LENGTH: int = os.getenv("CHATBOT_MAX_MESSAGE_LENGTH", 1000)
    CHATBOT_CONFIDENCE_THRESHOLD: float = os.getenv("CHATBOT_CONFIDENCE_THRESHOLD", 0.5)
    
    # Integration URLs
    CALENDAR_BOOKING_URL: Optional[str] = Field(None, env="CALENDAR_BOOKING_URL")
    CRM_WEBHOOK_URL: Optional[str] = Field(None, env="CRM_WEBHOOK_URL")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8000",
        # Add more frontend origins as needed
        "*"  # This allows any origin - for development only, remove in production!
    ]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
settings.SQLALCHEMY_DATABASE_URI = settings.get_database_uri



