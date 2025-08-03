from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Any
import yaml
from dataclasses import dataclass


@dataclass
class Configuration:
    model_config: Dict[str, Any]
    dictionary_terms: Dict[str, str]

    @classmethod
    def from_yaml(cls) -> 'Configuration':
        """Creates Configuration instance from YAML files"""
        model_config = ConfigLoader.load_yaml_file('model_configuration.yaml')
        dictionary = ConfigLoader.load_yaml_file('dictionary.yaml')

        if 'board_game_terms' not in dictionary:
            raise ValueError("Invalid dictionary format: 'board_game_terms' key not found")

        return cls(
            model_config=model_config,
            dictionary_terms=dictionary['board_game_terms']
        )


class ConfigLoader:
    @staticmethod
    def load_yaml_file(filename: str) -> Dict[str, Any]:
        """
        Load and parse a YAML configuration file.

        Args:
            filename: Name of the YAML file to load

        Returns:
            Parsed YAML content as dictionary

        Raises:
            FileNotFoundError: If configuration file is not found
            yaml.YAMLError: If YAML parsing fails
        """
        project_root = Path(__file__).resolve().parent
        config_path = project_root / 'config' / filename

        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{filename}' not found in {config_path}"
            )
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file '{filename}': {e}")


@lru_cache()
def get_configuration() -> Configuration:
    """Returns a cached instance of Configuration."""
    return Configuration.from_yaml()


# Public interface - keeps backward compatibility
def load_config() -> Dict[str, Any]:
    """Load model configuration."""
    return get_configuration().model_config


def load_dictionary() -> List[str]:
    """Load and format dictionary terms."""
    terms = get_configuration().dictionary_terms
    return [f"{key} -> {value}" for key, value in terms.items()]