import os
from langchain_groq import ChatGroq

# Initialize the LLM once and import it in other files
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192" # Using a standard, recommended model for Groq
)
