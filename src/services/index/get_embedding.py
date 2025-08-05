from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from src.config.model_config import load_config

@lru_cache()
def get_embedding() -> OpenAIEmbeddings:
    """Returns a cached OpenAI embeddings instance."""
    config = load_config()

    return OpenAIEmbeddings(model=config['embedding']['model'])