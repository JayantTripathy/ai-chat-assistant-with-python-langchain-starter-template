# app.py
import streamlit as st
import uuid
import os
from chatbot import build_chatbot_chain, generate_chatbot_response

# Set up the main page details
st.set_page_config(
    page_title="LLM Chat Companion",
    page_icon="🧠"
)

# Main header for the web app
st.title("🧠 Conversational AI with GPT-4o")

# API Key Verification
if not os.getenv("OPENAI_API_KEY"):
    st.info("Please configure your OpenAI API Key in the environment (.env) file for proper functionality.")

# Sidebar: Details & Controls
st.sidebar.header("Chatbot Overview")
st.sidebar.markdown("""
Harnessing the strength of OpenAI's GPT-4o, this chatbot specializes in:
- Providing guidance only about Artificial Intelligence
- Keeping answers brief, accurate, and relevant
- Never posing questions back to the user
""")

# Chat Session Initialization
if "conv_id" not in st.session_state:
    st.session_state.conv_id = str(uuid.uuid4())
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Chatbot Initialization with Exception Management
if "agent" not in st.session_state:
    try:
        st.session_state.agent = build_chatbot_chain()
    except Exception as err:
        st.error(f"Startup failed: {str(err)}")
        st.session_state.agent = None

# Reset chat through sidebar
if st.sidebar.button("Reset Conversation"):
    st.session_state.chat_log = []
    st.rerun()

# Render Chat History
for entry in st.session_state.chat_log:
    with st.chat_message(entry["role"]):
        st.write(entry["content"])

# User Input Section
prompt = st.chat_input("Enter your AI-related query...")
if prompt:
    # Record user message
    st.session_state.chat_log.append({"role": "user", "content": prompt})

    # Show what the user typed
    with st.chat_message("user"):
        st.write(prompt)

    # Generate assistant reply and display
    with st.chat_message("assistant"):
        with st.spinner("Composing reply..."):
            if st.session_state.agent:
                reply = generate_chatbot_response(st.session_state.agent, prompt, st.session_state.chat_log)
                st.write(reply)
            else:
                reply = "System error: Chat agent not available. Check OpenAI API Key."
                st.error(reply)

    # Record AI response
    st.session_state.chat_log.append({"role": "assistant", "content": reply})
