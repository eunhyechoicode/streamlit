import pytest
from unittest.mock import patch

from embedding import (
    YAMLConfiguration,
    ServerlessSpecConfig,
)


@pytest.fixture
def mock_config():
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
def yaml_config(mock_config):
    return YAMLConfiguration(
        embedding_model=mock_config['embedding']['model'],
        embedding_dimension=mock_config['embedding']['dimension'],
        pinecone_metric=mock_config['pinecone']['metric'],
        serverless_spec=ServerlessSpecConfig(
            cloud=mock_config['pinecone']['spec']['serverless']['cloud'],
            region=mock_config['pinecone']['spec']['serverless']['region']
        ),
        text_chunk_size=mock_config['text_splitter']['chunk_size'],
        text_chunk_overlap=mock_config['text_splitter']['chunk_overlap']
    )


class TestServerlessSpecConfig:
    def test_from_dict_valid(self):
        data = {'cloud': 'aws', 'region': 'us-east-1'}
        config = ServerlessSpecConfig.from_dict(data)
        assert config.cloud == 'aws'
        assert config.region == 'us-east-1'

    def test_from_dict_invalid_type(self):
        with pytest.raises(ValueError, match="must be a dictionary"):
            ServerlessSpecConfig.from_dict([])

    def test_from_dict_missing_fields(self):
        with pytest.raises(ValueError, match="must contain 'cloud' and 'region'"):
            ServerlessSpecConfig.from_dict({'cloud': 'aws'})


class TestYAMLConfiguration:
    def test_from_yaml(self, mock_config):
        with patch('embedding.load_config', return_value=mock_config):
            config = YAMLConfiguration.from_yaml()
            assert config.embedding_model == mock_config['embedding']['model']
            assert config.embedding_dimension == mock_config['embedding']['dimension']
            assert config.pinecone_metric == mock_config['pinecone']['metric']
            assert config.serverless_spec.cloud == mock_config['pinecone']['spec']['serverless']['cloud']
            assert config.serverless_spec.region == mock_config['pinecone']['spec']['serverless']['region']
            assert config.text_chunk_size == mock_config['text_splitter']['chunk_size']
            assert config.text_chunk_overlap == mock_config['text_splitter']['chunk_overlap']