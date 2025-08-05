import streamlit as st

from src.config import AppConfig

def setup_page_config():
    """Configure the Streamlit page settings"""
    try:
        app_config = AppConfig.get_instance()
        st.set_page_config(
            page_title=app_config.title,
            page_icon=app_config.icon,
        )
        st.title(f"{app_config.icon} {app_config.title}")
        st.caption(app_config.caption)
    except Exception as e:
        st.error(f"Error configuring page: {str(e)}")
        # Optionally provide fallback configuration
        st.set_page_config(
            page_title="Flip7",
            page_icon="🎮",
        )