# app/services/rag/embeddings.py
from typing import List
import openai  # or your preferred embedding provider
import openai, dotenv
from app.llm.prompt_engineer import system_prompt, txt2json_prompt, save2db_prompt

CFG = dotenv.dotenv_values(".env")
age = 300 # seconds

client = openai.OpenAI(api_key = CFG['OPENAI_API_KEY'])
model = "gpt-4o"


class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model

    async def embed(self, texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            model=self.model,
            input=texts
        )
        embeddings = [item.embedding for item in response.data]

        for emb in embeddings:
            if len(emb) != 1536:
                raise ValueError("Invalid embedding dimension")

        return embeddings