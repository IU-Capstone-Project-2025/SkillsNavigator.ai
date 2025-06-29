from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    embedding_model: str = "cointegrated/LaBSE-en-ru"


settings = Settings()


def setup_logging():
    import logging

    # Лог в консоль + в файл
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler("/app/log.log", mode='a'),
            logging.StreamHandler()
        ]
    )

    # Отключаем логи от httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
