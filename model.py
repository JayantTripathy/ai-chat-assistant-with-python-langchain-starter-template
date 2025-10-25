# model.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load all environment variables from .env file for secure API key handling
load_dotenv()

def initialize_openai_chat_model():
    """
    Initialize and return the OpenAI chat model with specified parameters
    for advanced chatbot generation.
    """
    return ChatOpenAI(
        model_name="gpt-4o-2024-11-20",
        temperature=0.75,  # Slightly creative response variation
        max_tokens=1500    # Set maximum token limit for responses
    )

def get_language_model_instance():
    """
    Provide the initialized OpenAI chat model instance for use in the app.
    """
    return initialize_openai_chat_model()
