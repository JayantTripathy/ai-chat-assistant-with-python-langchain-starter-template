# chatbot.py
from typing import List, Dict, Union
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from model import get_language_model_instance

def build_chatbot_chain():
    """Initialize the chatbot chain using the configured language model."""
    llm_instance = get_language_model_instance()
    
    system_instructions = """
    You are a helpful and polite AI assistant focused exclusively on Artificial Intelligence topics.
    Please respond clearly and concisely to user queries without asking questions.
    Use bullet points only for clarity and respond courteously to greetings or thanks.
    For unrelated topics, reply: 'I specialize in AI topics only. Could you please ask an AI-related question?'
    """
    
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_instructions),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_query}")
    ])
    
    conversation_chain = prompt_template | llm_instance
    return conversation_chain

def generate_chatbot_response(chain, input_text: str, conversation_history: List[Dict[str, Union[str, Dict]]] = None) -> str:
    """Generate a chatbot response for the provided input text and conversation history."""
    try:
        formatted_history = []
        if conversation_history:
            # Skip last user input (will add separately)
            for message in conversation_history[:-1]:
                if message["role"] == "user":
                    formatted_history.append(HumanMessage(content=message["content"]))
                elif message["role"] == "assistant":
                    formatted_history.append(AIMessage(content=message["content"]))
        
        response = chain.invoke({
            "chat_history": formatted_history,
            "user_query": input_text
        })
        
        if hasattr(response, "content"):
            return response.content
        return str(response)
        
    except Exception as error:
        return f"Sorry, I encountered an error: {str(error)}. Please try again."
