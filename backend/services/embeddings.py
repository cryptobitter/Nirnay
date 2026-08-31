from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from config import settings

def get_embedding_model() -> BaseEmbedding:
    """
    Initializes and returns the configured LlamaIndex OpenAI embedding model.
    Raises an error if the OpenAI API key is missing or invalid to prevent
    dimension mismatch corruption in the vector store.
    """
    if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.startswith("sk-"):
        raise ValueError("OPENAI_API_KEY is missing or invalid — Nirnay requires a valid OpenAI API key for embeddings.")

    return OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY
    )