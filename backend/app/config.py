from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    embedding_model: str = "cointegrated/LaBSE-en-ru"


settings = Settings()
