import os
from functools import lru_cache
from src.config.model_config import load_config


def get_project_root():
    """Get the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # src/services/index
    index_dir = os.path.dirname(current_dir)  # src/services
    services_dir = os.path.dirname(index_dir)  # src
    src_dir = os.path.dirname(services_dir)  # project root
    return src_dir  # returns the streamlit directory


@lru_cache()
def get_base_directory():
    """Get the base directory for board games."""
    config = load_config()
    relative_path = config['paths']['board_games_dir']
    project_root = get_project_root()
    absolute_path = os.path.join(project_root, relative_path)
    return absolute_path


def list_board_game_indices():
    """List all board game directories in the base directory."""
    base_directory = get_base_directory()
    if not os.path.exists(base_directory):
        print(f"Directory does not exist: {base_directory}")
        return []

    try:
        contents = os.listdir(base_directory)
        return [folder for folder in contents
                if os.path.isdir(os.path.join(base_directory, folder))]
    except Exception as e:
        print(f"Error while listing directory: {e}")
        return []