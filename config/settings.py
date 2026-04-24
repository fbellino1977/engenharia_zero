from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    # Locates the .env file in the root directory where the app is launched
    model_config = SettingsConfigDict(env_file=".env")


# We instantiate the object here to import it elsewhere
settings = Settings()
