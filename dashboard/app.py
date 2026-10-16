import streamlit as st
import requests

from config import SERVER_URL

st.set_page_config(
    page_title="AI LAB V6",
    layout="wide"
)

st.title("🚀 AI LAB V6")

try:
    data = requests.get(
        f"{SERVER_URL}/status",
        timeout=5
    ).json()

    st.success("✅ AI Server Online")
    st.json(data)

except Exception as e:
    st.error(str(e))

    factory = requests.get(
        f"{SERVER_URL}/factory/status",
        timeout=5
    ).json()

    memory = requests.get(
        f"{SERVER_URL}/agent/memory/audit",
        timeout=5
    ).json()

except Exception as e:

    st.error(
        f"AI Server non raggiungibile\n\n{e}"
    )

    st.stop()