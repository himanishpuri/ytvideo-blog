# llm_config.py
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7
)
