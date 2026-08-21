from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    mongodb_uri: str = ""
    database_name: str = "madacv"
    jwt_secret: str = ""
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    frontend_url: str = ""
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
