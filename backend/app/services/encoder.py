from sentence_transformers import SentenceTransformer

from app.services import run_blocking
from app.config import settings

import os


class EncoderService:
    def __init__(self):
        self.model = None

    async def initialize(self):
        if os.path.exists('/models/'+settings.embedding_model):
            self.model = await run_blocking(SentenceTransformer, '/models/'+settings.embedding_model)
        else:
            self.model = await run_blocking(SentenceTransformer, settings.embedding_model)
            self.model.save('/models/'+settings.embedding_model)

    async def vectorize(self, text: str):
        return await run_blocking(self.model.encode, text)

encoder = EncoderService()
