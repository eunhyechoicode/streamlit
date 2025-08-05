from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from config import load_config


@dataclass
class LLMConfig:
    """Configuration data class for LLM settings"""
    model: str
    temperature: float

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'LLMConfig':
        """Create LLMConfig from raw configuration dictionary"""
        llm_config = config.get('llm', {})
        return cls(
            model=llm_config['model'],
            temperature=llm_config['temperature']
        )


class LLMService:
    """Service class for managing LLM instances"""
    _instance = None

    def __init__(self, config: LLMConfig):
        self._config = config

    @classmethod
    def get_instance(cls) -> 'LLMService':
        """Get or create singleton instance"""
        if cls._instance is None:
            config = LLMConfig.from_config(load_config())
            cls._instance = cls(config)
        return cls._instance

    def create_chat_model(self, *, use_temperature: bool = False) -> ChatOpenAI:
        """Create a ChatOpenAI instance with optional temperature setting"""
        params = {'model': self._config.model}
        if use_temperature:
            params['temperature'] = self._config.temperature
        return ChatOpenAI(**params)


# Public interface functions
@lru_cache()
def get_llm_model() -> str:
    """Gets the LLM model name from configuration"""
    return LLMService.get_instance()._config.model


def get_llm() -> ChatOpenAI:
    """Creates and returns a ChatOpenAI instance with default settings"""
    return LLMService.get_instance().create_chat_model()


def get_judge_llm() -> ChatOpenAI:
    """Creates and returns a ChatOpenAI instance for evaluation purposes"""
    return LLMService.get_instance().create_chat_model(use_temperature=True)