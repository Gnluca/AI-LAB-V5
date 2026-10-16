import streamlit as st
import requests
from config import SERVER_URL

st.set_page_config(
    page_title="AI LAB V6",
    layout="wide"
)

st.title("🚀 AI LAB V6")

try:
    # Stato server
    data = requests.get(
        f"{SERVER_URL}/status",
        timeout=5
    ).json()

    st.success("✅ AI Server Online")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Server", data.get("status", "N/D"))

    with col2:
        st.metric("Ollama", data.get("ollama", "N/D"))

    with col3:
        st.metric("Modello", data.get("model", "N/D"))

    st.subheader("Dettagli")
    st.json(data)

except Exception as e:
    st.error(
        f"❌ AI Server non raggiungibile\n\n{e}"
    )
    st.stop()