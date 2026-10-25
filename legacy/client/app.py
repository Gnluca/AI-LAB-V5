import streamlit as st
import requests

SERVER_URL = "http://127.0.0.1:8000"
API_URL = f"{SERVER_URL}/chat"


st.title("AI Server Client")

prompt = st.text_input("Messaggio")

if st.button("Invia"):

    r = requests.post(
        API_URL,
        json={"text": prompt}
    )

    data = r.json()

    st.markdown(data.get("response", "Nessuna risposta"))