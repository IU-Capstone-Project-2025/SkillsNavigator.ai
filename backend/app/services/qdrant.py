from typing import List

from qdrant_client import QdrantClient, models

from app.services import run_blocking, encoder


class QdrantService:
    def __init__(self):
        self.client = None

    def initialize(self, host: str, port: int):
        self.client = QdrantClient(host=host, port=port)
        if not self.client.collection_exists(collection_name="courses"):
            self.client.create_collection(
                collection_name="courses",
                vectors_config=models.VectorParams(size=encoder.get_sentence_embedding_dimension(), distance=models.Distance.COSINE),
            )

    async def search(self, query: List[float], collection_name: str, limit: int = 10) -> List[dict]:
        return (await run_blocking(self.client.query_points,
            collection_name=collection_name,
            query=query,
            limit=limit
        )).points


qdrant = QdrantService()