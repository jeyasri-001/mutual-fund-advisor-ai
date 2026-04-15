from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_explanation(risk_category, sip_amount, recommendations):

    funds_text = ", ".join([
        f"{f['fund_name']} ({f['allocation']}%)"
        for f in recommendations
    ])

    prompt = f"""
    User has a {risk_category} risk profile and invests ₹{sip_amount} monthly.

    Recommended portfolio:
    {funds_text}

    Explain in simple terms:
    - Why this portfolio suits them
    - Risk vs return
    - Keep it beginner friendly
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content