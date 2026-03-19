from pydantic_settings import BaseSettings,SettingsConfigDict



class Setting(BaseSettings):
    SECRET_KEY = "test-1234"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )



def get_settings():
    setting = Setting()
    return setting

