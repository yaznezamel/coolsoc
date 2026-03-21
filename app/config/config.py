from pydantic_settings import BaseSettings,SettingsConfigDict
import os

APP_ENV = os.getenv("ENVIRONMENT", "local")

class Setting(BaseSettings):
    ENVIRONMENT: str = APP_ENV



    # Security
    SECRET_KEY: str = "test-1234"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60



    DATABASE_URL: str
    REDIS_URL: str
    model_config = SettingsConfigDict(
        env_file = f".env.{APP_ENV}",
        env_file_encoding = "utf-8",
        extra= "ignore"
    )



def get_settings():
    setting = Setting()
    return setting

