from functools import lru_cache
from pinecone import ServerlessSpec
from src.config.model_config import load_config


@lru_cache()
def get_pinecone_config() -> dict:
    """Returns cached Pinecone model configuration."""
    config = load_config()
    pinecone_config = config['pinecone']
    serverless_config = pinecone_config['spec']['serverless']

    return {
        'dimension': config['embedding']['dimension'],
        'metric': pinecone_config['metric'],
        'spec': ServerlessSpec(
            cloud=serverless_config['cloud'],
            region=serverless_config['region']
        )
    }