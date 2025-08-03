import pytest
from pathlib import Path
from unittest.mock import mock_open, patch
from config import ConfigLoader, Configuration, get_configuration, load_config, load_dictionary


@pytest.fixture
def mock_model_config():
    return {
        'embedding': {
            'model': 'text-embedding-3-large',
            'dimension': 3072
        },
        'pinecone': {
            'metric': 'cosine',
            'spec': {
                'serverless': {
                    'cloud': 'aws',
                    'region': 'us-east-1'
                }
            }
        },
        'text_splitter': {
            'chunk_size': 1000,
            'chunk_overlap': 200
        }
    }


@pytest.fixture
def mock_dictionary():
    return {
        'board_game_terms': {
            'term1': 'definition1',
            'term2': 'definition2'
        }
    }


class TestConfigLoader:
    def test_load_yaml_file_success(self, mock_model_config):
        with patch('builtins.open', mock_open(read_data="some yaml content")):
            with patch('yaml.safe_load', return_value=mock_model_config):
                with patch('pathlib.Path.resolve', return_value=Path('/fake/path')):
                    result = ConfigLoader.load_yaml_file('model_configuration.yaml')
                    assert result == mock_model_config

    def test_load_yaml_file_not_found(self):
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError
            with patch('pathlib.Path.resolve', return_value=Path('/fake/path')):
                with pytest.raises(FileNotFoundError) as exc_info:
                    ConfigLoader.load_yaml_file('nonexistent.yaml')
                assert 'Configuration file' in str(exc_info.value)


class TestConfiguration:
    def test_from_yaml_success(self, mock_model_config, mock_dictionary):
        with patch('config.ConfigLoader.load_yaml_file') as mock_load:
            mock_load.side_effect = [mock_model_config, mock_dictionary]
            config = Configuration.from_yaml()

            assert config.model_config == mock_model_config
            assert config.dictionary_terms == mock_dictionary['board_game_terms']
            assert mock_load.call_count == 2

    def test_from_yaml_invalid_dictionary(self, mock_model_config):
        with patch('config.ConfigLoader.load_yaml_file') as mock_load:
            mock_load.side_effect = [mock_model_config, {}]
            with pytest.raises(ValueError) as exc_info:
                Configuration.from_yaml()
            assert 'board_game_terms' in str(exc_info.value)


@pytest.fixture
def mock_configuration(mock_model_config, mock_dictionary):
    return Configuration(
        model_config=mock_model_config,
        dictionary_terms=mock_dictionary['board_game_terms']
    )


class TestPublicInterface:
    def test_get_configuration_cached(self, mock_configuration):
        with patch('config.Configuration.from_yaml', return_value=mock_configuration):
            config1 = get_configuration()
            config2 = get_configuration()
            assert config1 is config2  # Test caching
            Configuration.from_yaml.assert_called_once()

    def test_load_config(self, mock_configuration):
        with patch('config.get_configuration', return_value=mock_configuration):
            result = load_config()
            assert result == mock_configuration.model_config

    def test_load_dictionary(self, mock_configuration):
        with patch('config.get_configuration', return_value=mock_configuration):
            result = load_dictionary()
            expected = [
                'term1 -> definition1',
                'term2 -> definition2'
            ]
            assert result == expected