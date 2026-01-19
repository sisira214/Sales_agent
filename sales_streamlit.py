# app.py
import streamlit as st
from Sales_langchain import run_agent

st.set_page_config(page_title="SmartShop Assistant", page_icon="🛍️", layout="centered")

st.title("🛍️ SmartShop Assistant")
st.caption("Your AI-powered electronics shopping assistant using OpenAI + LangChain")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about a product (e.g., 'Show me some smartphones')"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            response = run_agent(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
