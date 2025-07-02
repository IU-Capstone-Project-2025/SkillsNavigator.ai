from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    embedding_model: str = "cointegrated/LaBSE-en-ru"
    web_url: str = os.getenv("WEB_URL", "http://localhost:8080")


settings = Settings()
