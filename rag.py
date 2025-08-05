from langchain.retrievers import MultiVectorRetriever, ParentDocumentRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from typing import List
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import load_dictionary
from embedding import get_embedding
from examples import answer_examples
from index import list_board_game_indices
from llm_service_config import get_llm

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def create_retrievers() -> List[ParentDocumentRetriever]:
    embedding = get_embedding()
    indices = list_board_game_indices()

    if not indices:
        raise ValueError("No board game indices found")

    retrievers = []
    for index_name in indices:
        database = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embedding
        )
        retrievers.append(database.as_retriever(search_kwargs={'k': 4}))

    return retrievers


def get_retriever():
    retrievers = create_retrievers()

    if len(retrievers) == 1:
        return retrievers[0]

    # For multiple retrievers, we'll merge their results
    return MultiVectorRetriever(
        retrievers=[retriever.with_config({"context": retriever}) for retriever in retrievers],
        verbose=True
    )


def get_history_retriever():
    llm = get_llm()
    retriever = get_retriever()

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever


def get_dictionary_chain():
    dictionary = load_dictionary()

    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(f"""
        Please review the user's question and modify it according to our dictionary.
        If you determine that no changes are necessary, you can return the question as is.
        dictionary: {dictionary}

        question: {{question}}
    """)

    dictionary_chain = prompt | llm | StrOutputParser()

    return dictionary_chain


def get_rag_chain():
    llm = get_llm()
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{answer}"),
        ]
    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=answer_examples,
    )

    system_prompt = (
        "You are a super enthusiastic Board Game Master who loves Flip7! 🎮 "
        "You're here to make learning and playing the game fun for everyone! "
        "Use the following game info to help answer questions: {context}\n\n"
        "Keep your responses upbeat and friendly! Use emojis to make it fun! "
        "If you don't know something, just say 'Oops! I'm not sure about that one! 🤔' "
        "Start your answers with friendly phrases like:\n"
        "- 'Hey there! According to the rules...' ✨\n"
        "- 'Great question! The game guide says...' 🌟\n"
        "- 'Let me help you with that! In Flip7...' 🎲\n"
        "Keep answers short and sweet - 2-3 sentences max!"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = get_history_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ).pick('answer')

    return conversational_rag_chain


def get_ai_response(user_message):
    dictionary_chain = get_dictionary_chain()
    rag_chain = get_rag_chain()
    board_game_chain = {"input": dictionary_chain} | rag_chain
    ai_response = board_game_chain.stream(
        {
            "question": user_message
        },
        config={
            "configurable": {"session_id": "abc123"}
        },
    )

    return ai_response