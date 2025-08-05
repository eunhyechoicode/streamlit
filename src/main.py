from dotenv import load_dotenv
from .core.session import initialize_session_state
from .ui.layout import setup_page_config
from .core.chat import display_chat_history, handle_user_input

def main():
    """Main application entry point"""
    load_dotenv()

    initialize_session_state()
    setup_page_config()

    display_chat_history()
    handle_user_input()
