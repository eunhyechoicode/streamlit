from functools import lru_cache
from typing import Dict, Any
from .config_loader import ConfigLoader


class ModelConfig:
    _instance = None
    config: Dict[str, Any]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelConfig, cls).__new__(cls)
            cls._instance.config = ConfigLoader.load_yaml_file('model.yaml')
        return cls._instance

    @property
    def data(self) -> Dict[str, Any]:
        return self.config


@lru_cache()
def get_model_config() -> ModelConfig:
    """Returns singleton instance of ModelConfig."""
    return ModelConfig()


def load_config() -> Dict[str, Any]:
    """Load model configuration."""
    return get_model_config().data