import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'message_list' not in st.session_state:
        st.session_state.message_list = []