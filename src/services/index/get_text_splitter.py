from functools import lru_cache
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.model_config import load_config


@lru_cache()
def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """Returns a cached text splitter instance."""
    config = load_config()
    splitter_config = config['text_splitter']

    return RecursiveCharacterTextSplitter(
        chunk_size=splitter_config['chunk_size'],
        chunk_overlap=splitter_config['chunk_overlap'],
        length_function=len
    )