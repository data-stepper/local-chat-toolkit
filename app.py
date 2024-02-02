from openai import OpenAI
import streamlit as st

from src import format_model_name, get_model_list, load_model_instructions, save_new_model

chat, models_tab = st.tabs(["Chat", "Models"])

with models_tab:
    st.title("Models")
    st.caption("Create or edit models that make the chatbot smarter.")

    models = get_model_list()
    models.append("Create New Model")

    # Dropdown to select a model
    model: str = st.selectbox("Select a model", models)

    try:
        default_instructions = load_model_instructions(model)

    except FileNotFoundError:
        default_instructions = "Be precise and concise."

    with st.form("create_model"):
        model_name = st.text_input("Model Name", value=format_model_name(model))

        model_instructions = st.text_area("Instructions", value=default_instructions)
        model_create_button = st.form_submit_button("Create Model")

        if model_create_button:
            # Create and save new model
            save_new_model(model_name, model_instructions)


def set_default_messages(model_name: str):
    try:
        m = [{"role": "assistant", "content": load_model_instructions(model_name)}]

    except FileNotFoundError:
        m = [{"role": "assistant", "content": "Be precise and concise."}]

    if not "messages" in st.session_state:
        st.session_state["messages"] = m

    else:
        st.session_state["messages"] = m


def add_new_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

    with st.chat_message(role):
        st.write(content)


# setup a small sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    # Choose a model
    models_available = get_model_list()
    model = st.selectbox("Choose a model", models_available)
    instructions = load_model_instructions(model)
    set_default_messages(model)

    new_chat_button = st.button("Start a new chat")

    if new_chat_button:
        set_default_messages(model)


with chat:
    st.title("Chat Toolkit")
    st.caption("A chatbot with permanent templates.")

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    chat_input_field = st.chat_input("Type a message...", key="chat_input")

    if chat_input_field:
        add_new_message("user", chat_input_field)
        msg = "Hello, how are you?"
        add_new_message("assistant", msg)
