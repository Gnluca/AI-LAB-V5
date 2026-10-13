import streamlit as st
import requests

from config import SERVER_URL

st.set_page_config(
    page_title="AI LAB V5",
    layout="wide"
)

st.title("🚀 AI LAB V5")

# =====================
# STATUS
# =====================

status = requests.get(
    f"{SERVER_URL}/status"
).json()

factory = requests.get(
    f"{SERVER_URL}/factory/status"
).json()

memory = requests.get(
    f"{SERVER_URL}/agent/memory/audit"
).json()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Model",
        status["model"]
    )

with c2:
    st.metric(
        "Agents",
        factory["agents"]
    )

with c3:
    st.metric(
        "Memory",
        memory["memory_records"]
    )

with c4:
    st.metric(
        "Knowledge %",
        memory["coverage_percent"]
    )

st.divider()

try:

    status = requests.get(
        f"{SERVER_URL}/status",
        timeout=5
    ).json()

except Exception:

    st.error(
        f"AI Server non raggiungibile: {SERVER_URL}"
    )

    st.stop()


# =====================
# NETWORK
# =====================

st.header("Network")

network = requests.get(
    f"{SERVER_URL}/agent/network/discover"
).json()

st.json(network)

st.divider()

# =====================
# FACTORY
# =====================

st.header("Factory")

factory_list = requests.get(
    f"{SERVER_URL}/factory/list"
).json()

st.json(factory_list)

st.divider()

# =====================
# KNOWLEDGE
# =====================

st.header("Knowledge")

knowledge = requests.get(
    f"{SERVER_URL}/knowledge/list"
).json()

st.json(knowledge)

st.divider()

# =====================
# GOVERNANCE
# =====================

st.header("Governance")

gov = requests.get(
    f"{SERVER_URL}/agent/labmanager/governance"
).json()

st.text_area(
    "ARCHITETTURA.md",
    gov["governance"],
    height=400
)