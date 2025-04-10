from anthropic import Anthropic
from utils.config import ANTHROPIC_API_KEY

class AnthropicClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnthropicClient, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        from anthropic import Anthropic
        from utils.config import ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def answer_query_base(self, query: str, context_chunks: list[str], model="claude-3-haiku-20240307") -> str:
        context = "\n\n".join(context_chunks)
        prompt = f"""
        You have been tasked with helping us to answer the following query:
        <query>
        {query}
        </query>
        You have access to the following documents which are meant to provide context as you answer the query:
        <documents>
        {context}
        </documents>
        Please remain faithful to the underlying context, and only deviate from it if you are 100% sure that you know the answer already.
        Answer the question now, and avoid providing preamble such as 'Here is the answer', etc.
        """

        response = self.client.messages.create(
            model=model,
            max_tokens=2500,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

