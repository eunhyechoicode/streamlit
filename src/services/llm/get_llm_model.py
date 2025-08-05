from functools import lru_cache
from src.config.model_config import load_config


@lru_cache()
def get_llm_model() -> str:
    """Returns a cached LLM model name from configuration."""
    config = load_config()
    return config['llm']['model']