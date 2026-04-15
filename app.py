import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from engine.risk_engine import calculate_risk_score, get_risk_category
from engine.recommender import get_recommendation
from chatbot.explainer import generate_explanation
from chatbot.rag_chat import rag_response

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Fund Advisor", layout="centered")

# ---------------------------
# CUSTOM UI
# ---------------------------
st.markdown("""
<style>
.block-container {
    max-width: 720px;
    padding-top: 2rem;
}

h1, h2, h3 {
    text-align: center;
}

div[data-testid="stButton"] > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #2962ff;
    color: white;
    font-weight: bold;
    border: none;
}

.card {
    background-color:#1e1e1e;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
    border:1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs(["📋 Guided Advisor", "🤖 AI Advisor"])

# =====================================================
# 📋 GUIDED ADVISOR
# =====================================================
with tab1:

    st.title("📊 Smart Mutual Fund Advisor")
    st.write("Answer a few questions to get your personalized portfolio")

    # Q1
    q1 = st.radio(
        "1. Investment experience?",
        ["Never", "Less than 2 years", "2-4 years", "4+ years"]
    )

    q1_score_map = {
        "Never": 10,
        "Less than 2 years": 40,
        "2-4 years": 70,
        "4+ years": 100
    }

    # Q2
    q2 = st.multiselect(
        "2. Investments done?",
        ["None", "PPF/EPF/FD", "Gold/Real Estate", "NPS", "Stocks", "AIF/PMS", "Crypto"]
    )

    q2_score_map = {
        "None": 10,
        "PPF/EPF/FD": 30,
        "Gold/Real Estate": 40,
        "NPS": 50,
        "Stocks": 80,
        "AIF/PMS": 90,
        "Crypto": 100
    }

    q2_score = max([q2_score_map.get(i, 0) for i in q2]) if q2 else 10

    # Q3
    q3 = st.radio(
        "3. What matters more?",
        ["Safety First", "Balanced", "Growth Focus"]
    )

    q3_score_map = {
        "Safety First": 20,
        "Balanced": 60,
        "Growth Focus": 100
    }

    # Q4
    q4 = st.multiselect(
        "4. Current liabilities?",
        ["Loan", "Dependent", "Insurance Premium", "None"]
    )

    if "Loan" in q4:
        q4_score = 20
    elif "Dependent" in q4:
        q4_score = 50
    else:
        q4_score = 80

    # SIP
    sip_amount = st.number_input(
        "Monthly SIP Amount (₹)",
        min_value=1000,
        value=30000,
        step=500
    )

    st.write(f"💰 SIP: ₹{sip_amount:,}")

    # BUTTON
    if st.button("Get My Portfolio"):

        scores = [
            q1_score_map[q1],
            q2_score,
            q3_score_map[q3],
            q4_score,
            80
        ]

        weights = [13, 14, 20, 13, 10]

        risk_score = calculate_risk_score(scores, weights)
        risk_category = get_risk_category(risk_score)

        recommendations = get_recommendation(risk_category, sip_amount)

        st.success(f"🎯 Risk Profile: {risk_category.upper()}")

        if recommendations:

            df = pd.DataFrame(recommendations)

            st.subheader("💼 Recommended Portfolio")

            for fund in recommendations:
                st.markdown(f"""
                <div class="card">
                    <h4>{fund['fund_name']}</h4>
                    <p>Allocation: <b>{fund['allocation']}%</b></p>
                </div>
                """, unsafe_allow_html=True)

            # PIE CHART
            st.subheader("📊 Portfolio Allocation")

            fig, ax = plt.subplots()
            ax.pie(df["allocation"], autopct="%1.0f%%")
            ax.set_title("Portfolio Split")

            st.pyplot(fig)

            # AI EXPLANATION
            st.subheader("🤖 AI Insight")

            explanation = generate_explanation(
                risk_category,
                sip_amount,
                recommendations
            )

            st.write(explanation)

        else:
            st.warning("No recommendations found.")

# =====================================================
# 🤖 AI ADVISOR (FIXED CHAT)
# =====================================================
with tab2:

    st.title("🤖 AI Financial Advisor")
    st.write("Ask anything about mutual funds")

    # INIT STATE
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # DISPLAY CHAT HISTORY (ONLY SOURCE OF UI)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # INPUT
    user_input = st.chat_input("Type your question...")

    if user_input:

        # STORE USER MESSAGE
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # AI RESPONSE (with loader)
        with st.spinner("Thinking..."):
            response = rag_response(user_input)

        # STORE BOT MESSAGE
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        # REFRESH UI (prevents duplicate)
        st.rerun()