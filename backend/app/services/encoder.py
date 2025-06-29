import logging
import torch
from sentence_transformers import SentenceTransformer

from app.services import run_blocking
from app.config import settings

logger = logging.getLogger(__name__)


class EncoderService:
    def __init__(self):
        self.model = None

    async def initialize(self):
        try:
            logger.info(f"Init model: {settings.embedding_model}")
            self.model = await run_blocking(SentenceTransformer, settings.embedding_model, cache_folder="models/")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(device)
            logger.info(f"Model loaded and set up: {device}")
        except Exception as e:
            logger.exception("Error model vectorization")
            raise

    async def vectorize(self, text: str):
        try:
            logger.debug(f"Vectorize text of length {len(text)}")
            return await run_blocking(self.model.encode, text, show_progress_bar=False)
        except Exception as e:
            logger.exception("Error Vectorization")
            raise


encoder = EncoderService()
