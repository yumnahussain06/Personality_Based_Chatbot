import os
import streamlit as st

from main import (
    MODELS,
    PERSONALITIES,
    chat_with_model
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Personality Based Chatbot",
    layout="wide"
)

st.title("Personality Based Chatbot")
st.caption("Powered by Groq AI")


# --------------------------------------------------
# API Key Check
# --------------------------------------------------

if not os.getenv("GROQ_API_KEY"):
    st.error("Groq API Key not found.")
    st.info("Please add GROQ_API_KEY inside your .env file.")
    st.stop()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Settings")

    selected_model = st.selectbox(
        "Choose Model",
        MODELS
    )

    selected_personality = st.selectbox(
        "Choose Personality",
        list(PERSONALITIES.keys())
    )

    st.divider()

    clear_chat = st.button(
        "🗑 Clear Conversation",
        use_container_width=True
    )

    st.divider()

    st.markdown(
        """
        ### Current Personality

        The chatbot will answer only within
        the selected personality.

        Questions outside its expertise
        should be politely refused.
        """
    )


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "previous_personality" not in st.session_state:

    st.session_state.previous_personality = selected_personality


# --------------------------------------------------
# Personality Changed
# --------------------------------------------------

if selected_personality != st.session_state.previous_personality:

    st.session_state.messages = []

    st.session_state.previous_personality = selected_personality

    st.success(
        f"Conversation reset.\n\nPersonality changed to **{selected_personality}**."
    )

    st.rerun()


# --------------------------------------------------
# Clear Chat
# --------------------------------------------------

if clear_chat:

    st.session_state.messages = []

    st.rerun()


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input(
    "Type your message..."
)


if prompt:

    prompt = prompt.strip()

    if len(prompt) == 0:

        st.warning("Please enter a valid message.")

        st.stop()


    # ----------------------------------------------
    # Display User Message
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)


    # ----------------------------------------------
    # Store User Message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # ----------------------------------------------
    # Limit Conversation Length
    # Keeps recent context only
    # ----------------------------------------------

    MAX_MESSAGES = 20

    if len(st.session_state.messages) > MAX_MESSAGES:

        st.session_state.messages = (
            st.session_state.messages[-MAX_MESSAGES:]
        )


    # ----------------------------------------------
    # Assistant Response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
                try:

                    response = chat_with_model(

                        user_message=prompt,

                        personality=selected_personality,

                        model=selected_model,

                        chat_history=st.session_state.messages[:-1]

                    )

                    st.markdown(response)

                except Exception:

                    response = None

                    st.error(
                        "Unable to connect to the AI service. "
                        "Please check your internet connection or try again later."
                    )


        # ----------------------------------------------
        # Store Assistant Response
        # ----------------------------------------------

        if response:

            st.session_state.messages.append(

                {
                    "role": "assistant",
                    "content": response
                }

            )