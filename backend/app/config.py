from pydantic_settings import BaseSettings
import logging
import os

class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    embedding_model: str = "cointegrated/LaBSE-en-ru"
    web_url: str = os.getenv("WEB_URL", "http://localhost:8080")
    secret_key: str = os.getenv("", "somerandomkey")


settings = Settings()


def setup_logging():
    log_path = "app/log.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Создаём файл, если его нет (без записи)
    if not os.path.exists(log_path):
        with open(log_path, "a"):
            pass

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode='a'),
            logging.StreamHandler()
        ]
    )

    # Отключаем логи от httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
