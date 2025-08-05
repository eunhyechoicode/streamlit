import streamlit as st

from src.config import AppConfig
from src.services.rag import get_ai_response

def display_chat_history():
    """Display all messages in the chat history"""
    for message in st.session_state.message_list:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def handle_user_input():
    """Process user input and generate AI response"""

    app_config = AppConfig.get_instance()
    placeholder = app_config.chat_placeholder
    loading_message = app_config.loading_message

    if user_question := st.chat_input(placeholder):
        # Display user message
        with st.chat_message("user"):
            st.write(user_question)
        st.session_state.message_list.append({"role": "user", "content": user_question})

        # Generate and display AI response
        with st.spinner(loading_message):
            # ai_response = "Hello, I am a chatbot that can help you with Flip7 game rules and strategies!"
            ai_response = get_ai_response(user_question)
            with st.chat_message("ai"):
                ai_message = st.write_stream(ai_response)
                # ai_message = st.write(ai_response)
                st.session_state.message_list.append({"role": "ai", "content": ai_message})
