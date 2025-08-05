from dataclasses import dataclass
from typing import ClassVar
from .config_loader import ConfigLoader


@dataclass
class AppConfig:
    title: str
    icon: str
    caption: str
    chat_placeholder: str
    loading_message: str

    _instance: ClassVar = None

    @classmethod
    def get_instance(cls) -> 'AppConfig':
        if not cls._instance:
            cls._instance = cls.from_yaml()
        return cls._instance

    @classmethod
    def from_yaml(cls) -> 'AppConfig':
        try:
            config = ConfigLoader.load_yaml_file('app.yaml')
            app_config = config.get('app', {})
            chat_config = config.get('chat', {})
            return cls(
                title=app_config['title'],
                icon=app_config['icon'],
                caption=app_config['caption'],
                chat_placeholder=chat_config['placeholder'],
                loading_message=chat_config['loading_message']
            )
        except (FileNotFoundError, KeyError):
            return cls(
                title="Flip7",
                icon="🎮",
            )