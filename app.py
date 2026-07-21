import streamlit as st

from main import (
    MODELS,
    PERSONALITIES,
    chat_with_model
)


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Personality Based Chatbot",
    layout="wide"
)

st.title("Personality Based Chatbot")
st.markdown("Choose a model and personality, then start chatting!")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("Settings")

    selected_model = st.selectbox(
        "Select Model",
        MODELS
    )

    selected_personality = st.selectbox(
        "Select Personality",
        list(PERSONALITIES.keys())
    )

    st.divider()

    clear_chat = st.button("🗑️ Clear Chat")


# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Clear Chat
# -----------------------------
if clear_chat:
    st.session_state.messages = []
    st.rerun()


# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Type your message...")


if prompt:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Generate Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = chat_with_model(
                user_message=prompt,
                personality=selected_personality,
                model=selected_model,
                chat_history=st.session_state.messages[:-1]
            )

        st.markdown(response)

    # Save Assistant Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )