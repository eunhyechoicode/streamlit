from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Optional

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import ServerlessSpec
from dotenv import load_dotenv

from config import load_config

load_dotenv()


@dataclass
class ServerlessSpecConfig:
    cloud: str
    region: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'ServerlessSpecConfig':
        if not isinstance(data, dict):
            raise ValueError("Serverless spec configuration must be a dictionary")
        if 'cloud' not in data or 'region' not in data:
            raise ValueError("Serverless spec must contain 'cloud' and 'region'")
        return cls(cloud=data['cloud'], region=data['region'])


@dataclass
class YAMLConfiguration:
    embedding_model: str
    embedding_dimension: int
    pinecone_metric: str
    serverless_spec: ServerlessSpecConfig
    text_chunk_size: int
    text_chunk_overlap: int

    @classmethod
    def from_yaml(cls) -> 'YAMLConfiguration':
        config = load_config()

        if 'embedding' not in config:
            raise ValueError("Missing 'embedding' section in configuration")
        if 'pinecone' not in config:
            raise ValueError("Missing 'pinecone' section in configuration")
        if 'text_splitter' not in config:
            raise ValueError("Missing 'text_splitter' section in configuration")

        embedding_config = config['embedding']
        pinecone_config = config['pinecone']
        text_splitter_config = config['text_splitter']

        return cls(
            embedding_model=embedding_config['model'],
            embedding_dimension=embedding_config['dimension'],
            pinecone_metric=pinecone_config['metric'],
            serverless_spec=ServerlessSpecConfig.from_dict(
                pinecone_config['spec']['serverless']
            ),
            text_chunk_size=text_splitter_config['chunk_size'],
            text_chunk_overlap=text_splitter_config['chunk_overlap']
        )


class ModelFactory:
    def __init__(self, config: YAMLConfiguration):
        self._config = config
        self._embedding: Optional[OpenAIEmbeddings] = None
        self._text_splitter: Optional[RecursiveCharacterTextSplitter] = None

    def get_embedding(self) -> OpenAIEmbeddings:
        if not self._embedding:
            self._embedding = OpenAIEmbeddings(model=self._config.embedding_model)
        return self._embedding

    def get_pinecone_model(self) -> dict:
        return {
            'dimension': self._config.embedding_dimension,
            'metric': self._config.pinecone_metric,
            'spec': ServerlessSpec(
                cloud=self._config.serverless_spec.cloud,
                region=self._config.serverless_spec.region
            )
        }

    def get_text_splitter(self) -> RecursiveCharacterTextSplitter:
        if not self._text_splitter:
            self._text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self._config.text_chunk_size,
                chunk_overlap=self._config.text_chunk_overlap,
                length_function=len
            )
        return self._text_splitter


@lru_cache()
def get_model_factory() -> ModelFactory:
    """Returns a cached instance of ModelFactory."""
    config = YAMLConfiguration.from_yaml()
    return ModelFactory(config)


# Public interface - keeps backward compatibility
def get_embedding() -> OpenAIEmbeddings:
    return get_model_factory().get_embedding()


def get_pinecone_model() -> dict:
    return get_model_factory().get_pinecone_model()


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    return get_model_factory().get_text_splitter()