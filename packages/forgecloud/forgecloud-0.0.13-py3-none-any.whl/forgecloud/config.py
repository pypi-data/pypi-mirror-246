from pydantic import BaseSettings

from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    """Server config settings."""
    api_key: str


settings = Settings()