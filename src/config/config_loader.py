from pathlib import Path
from typing import Dict, Any
import yaml


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
        current_path = Path(__file__).resolve()
        # Use the resolved base path's parent.parent/yaml/filename
        config_path = current_path.parent.parent / 'yaml' / filename

        try:
            with open(config_path, 'r') as file:
                content = yaml.safe_load(file)
                return content if content else None
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{filename}' not found in {config_path}"
            )
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file '{filename}': {e}")