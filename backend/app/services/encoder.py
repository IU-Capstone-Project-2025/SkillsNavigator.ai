from sentence_transformers import SentenceTransformer

from app.services import run_blocking
from app.config import settings

import os


class EncoderService:
    def __init__(self):
        self.model = None

    async def initialize(self):
        self.model = await run_blocking(SentenceTransformer, settings.embedding_model, cache_folder="models/")

    async def vectorize(self, text: str):
        return await run_blocking(self.model.encode, text)

encoder = EncoderService()
