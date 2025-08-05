
from functools import lru_cache
from langchain_openai import ChatOpenAI
from src.services.llm.get_llm_model import get_llm_model


class LLM:
    """Singleton class for managing the LLM instance."""
    _instance = None

    def __init__(self):
        if LLM._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        self.llm = ChatOpenAI(
            model_name=get_llm_model()
        )

    @classmethod
    @lru_cache()
    def get_instance(cls) -> ChatOpenAI:
        """Get or create the singleton LLM instance."""
        if cls._instance is None:
            cls._instance = LLM()
        return cls._instance.llm


def get_llm() -> ChatOpenAI:
    """Creates and returns a cached ChatOpenAI instance."""
    return LLM.get_instance()