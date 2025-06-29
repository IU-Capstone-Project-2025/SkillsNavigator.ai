from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    embedding_model: str = "cointegrated/LaBSE-en-ru"


settings = Settings()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )

    # Отключаем логи от httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
