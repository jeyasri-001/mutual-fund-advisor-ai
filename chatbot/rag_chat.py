from groq import Groq
import os
from dotenv import load_dotenv
from chatbot.rag import search_funds
import streamlit as st

load_dotenv()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def rag_response(user_query):

    context_data = search_funds(user_query)

    context = f"Relevant fund data: {context_data}"

    prompt = f"""
You are a financial advisor.

Use the data if available. If not, still answer intelligently using general knowledge.

Context:
{context}

User Question: {user_query}

Rules:
- NEVER say "I don't have information"
- Always give a helpful answer
- Keep it simple and professional
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content