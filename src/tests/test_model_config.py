import pytest
from unittest.mock import patch, MagicMock
from src.config.model_config import ModelConfig, get_model_config, load_config


class TestModelConfig:
    @pytest.fixture
    def mock_config_data(self):
        return {
            "embedding": {
                "model": "text-embedding-3-large",
                "dimension": 3072
            },
            "pinecone": {
                "metric": "cosine",
                "spec": {
                    "serverless": {
                        "cloud": "aws",
                        "region": "us-east-1"
                    }
                }
            },
            "llm": {
                "model": "gpt-4o",
                "temperature": 0
            },
            "paths": {
                "board_games_dir": "board-games"
            },
            "text_splitter": {
                "chunk_size": 1000,
                "chunk_overlap": 200
            }
        }

    def test_singleton_pattern(self):
        """Test that ModelConfig maintains singleton pattern"""
        config1 = ModelConfig()
        config2 = ModelConfig()
        assert config1 is config2

    def test_get_model_config_caching(self):
        """Test that get_model_config uses caching"""
        config1 = get_model_config()
        config2 = get_model_config()
        assert config1 is config2

    @patch('src.config.model_config.ConfigLoader')
    def test_load_config(self, mock_loader, mock_config_data):
        """Test load_config returns correct data"""
        mock_loader.load_yaml_file.return_value = mock_config_data

        # Reset singleton instance for testing
        ModelConfig._instance = None

        # Create mock instance
        mock_instance = MagicMock()
        mock_instance.config = mock_config_data
        ModelConfig._instance = mock_instance

        config_data = load_config()
        assert config_data == mock_config_data

    @patch('src.config.model_config.ConfigLoader')
    def test_config_loading_error(self, mock_loader):
        """Test error handling during config loading"""
        mock_loader.load_yaml_file.side_effect = FileNotFoundError(
            "Configuration file 'model.yaml' not found"
        )

        # Reset singleton instance
        ModelConfig._instance = None

        with pytest.raises(FileNotFoundError) as exc:
            ModelConfig()
        assert "Configuration file 'model.yaml' not found" in str(exc.value)

    def test_data_property(self, mock_config_data):
        """Test the data property returns correct config"""
        # Reset singleton instance
        ModelConfig._instance = None

        # Create instance with mock data
        instance = ModelConfig()
        instance.config = mock_config_data

        assert instance.data == mock_config_data
        assert get_model_config().data == mock_config_data