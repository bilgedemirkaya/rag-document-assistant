import voyageai
from utils.config import VOYAGE_API_KEY

class EmbeddingClient:
    def __init__(self):
        self.client = voyageai.Client(api_key=VOYAGE_API_KEY)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        result = self.client.embed(texts, model="voyage-2", input_type="document")
        return result.embeddings


embedding_client = EmbeddingClient()
