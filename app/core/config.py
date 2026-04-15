import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "SUPER_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"

    class Config:
        from_attributes = True  # Pydantic V2 için

settings = Settings()
