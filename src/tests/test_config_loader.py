import pytest
from unittest.mock import mock_open, patch
import yaml

from src.config.config_loader import ConfigLoader


@pytest.fixture
def yaml_content():
    return {"app": {"title": "Test App"}, "settings": {"debug": True}}


class TestConfigLoader:
    def test_load_success(self, yaml_content):
        with patch('builtins.open', mock_open(read_data="content")):
            with patch('yaml.safe_load', return_value=yaml_content):
                result = ConfigLoader.load_yaml_file('config.yaml')
                assert result == yaml_content

    def test_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError()):
            with pytest.raises(FileNotFoundError) as exc:
                ConfigLoader.load_yaml_file('missing.yaml')
            assert 'Configuration file' in str(exc.value)

    def test_yaml_error(self):
        with patch('builtins.open', mock_open(read_data="invalid: :")):
            with patch('yaml.safe_load', side_effect=yaml.YAMLError()):
                with pytest.raises(yaml.YAMLError) as exc:
                    ConfigLoader.load_yaml_file('invalid.yaml')
                assert 'Error parsing YAML file' in str(exc.value)

    def test_empty_file(self):
        with patch('builtins.open', mock_open(read_data="")):
            result = ConfigLoader.load_yaml_file('empty.yaml')
            assert result is None
