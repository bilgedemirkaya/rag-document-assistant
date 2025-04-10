import voyageai
from utils.config import VOYAGE_API_KEY

class EmbeddingClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingClient, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.client = voyageai.Client(api_key=VOYAGE_API_KEY)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        result = self.client.embed(texts, model="voyage-2", input_type="document")
        return result.embeddings
