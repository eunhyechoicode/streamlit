from functools import lru_cache
from langchain_openai import ChatOpenAI
from src.config.model_config import load_config


class JudgeLLM:
    """Singleton class for managing the judge LLM instance."""
    _instance = None

    def __init__(self):
        if JudgeLLM._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        config = load_config()
        self.llm = ChatOpenAI(
            model=config['llm']['model'],
            temperature=config['llm']['temperature']
        )

    @classmethod
    @lru_cache()
    def get_instance(cls) -> ChatOpenAI:
        """Get or create the singleton LLM instance."""
        if cls._instance is None:
            cls._instance = JudgeLLM()
        return cls._instance.llm


def get_judge_llm() -> ChatOpenAI:
    """Creates and returns a cached ChatOpenAI instance for evaluation purposes."""
    return JudgeLLM.get_instance()