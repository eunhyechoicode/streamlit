from functools import lru_cache
from typing import Dict, List
from .config_loader import ConfigLoader


class Dictionary:
    _instance = None
    terms: Dict[str, str]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Dictionary, cls).__new__(cls)
            dictionary = ConfigLoader.load_yaml_file('dictionary.yaml')
            if 'board_game_terms' not in dictionary:
                raise ValueError("Invalid dictionary format: 'board_game_terms' key not found")
            cls._instance.terms = dictionary['board_game_terms']
        return cls._instance

    def get_formatted_terms(self) -> List[str]:
        """Returns dictionary terms in formatted string list."""
        return [f"{key} -> {value}" for key, value in self.terms.items()]

    @property
    def data(self) -> Dict[str, str]:
        return self.terms


@lru_cache()
def get_dictionary() -> Dictionary:
    """Returns singleton instance of Dictionary."""
    return Dictionary()


def load_dictionary() -> List[str]:
    """Load and format dictionary terms."""
    return get_dictionary().get_formatted_terms()