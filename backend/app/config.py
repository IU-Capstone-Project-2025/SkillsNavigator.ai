from pydantic_settings import BaseSettings
import logging
import os


class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    embedding_model: str = "cointegrated/LaBSE-en-ru"
    deepseek_api_key: str = ""
    deepseek_api_url: str = "https://api.deepseek.com/v1/chat/completions"
    similarity_threshold: float = 0  # Lowered from 0.7 to 0.6 for better course matching
    load_courses: str = "false"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Try to get API key from environment variable if not set
        if not self.deepseek_api_key:
            self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
        
        # Allow similarity threshold to be overridden by environment variable
        env_threshold = os.getenv("SIMILARITY_THRESHOLD")
        if env_threshold:
            try:
                self.similarity_threshold = float(env_threshold)
            except ValueError:
                logger.warning(f"Invalid SIMILARITY_THRESHOLD value: {env_threshold}, using default: {self.similarity_threshold}")


settings = Settings()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )

    # Отключаем логи от httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
