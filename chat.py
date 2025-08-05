import streamlit as st
from dotenv import load_dotenv

from rag import get_ai_response

load_dotenv()

st.set_page_config(page_title="Flip7 Game Master", page_icon="🃏")
st.title("🃏 Flip7 Game Master")
st.caption("Ask anything about Flip7 game rules and strategies!")

if 'message_list' not in st.session_state:
    st.session_state.message_list = []


for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if user_question := st.chat_input(placeholder="Ask me anything about Flip7!"):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    with st.spinner("🌟Flipping through the rule book..."):
        ai_response = get_ai_response(user_question)
        with st.chat_message("ai"):
            ai_message = st.write_stream(ai_response)
            st.session_state.message_list.append({"role": "ai", "content": ai_message })