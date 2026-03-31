import streamlit as st
from agent_team import run_agent

st.set_page_config(page_title="AI Finance Agent", layout="wide")

st.title("📊 AI Multi-Agent Finance System")

# Sidebar
st.sidebar.header("Try:")
st.sidebar.markdown("""
- What is TSLA stock price?
- What if Tesla grows 15%?
- Latest AI news
- Should I invest in Nvidia?
""")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your query:")

col1, col2 = st.columns(2)
run = col1.button("Run")
clear = col2.button("Clear")

if clear:
    st.session_state.history = []

if run and query:
    with st.spinner("Processing..."):
        try:
            response = run_agent(query)
            st.session_state.history.append((query, response))
        except Exception as e:
            st.error(str(e))

# Display chat
st.subheader("Conversation")

for q, r in reversed(st.session_state.history):
    st.markdown(f"🧑 **You:** {q}")
    st.markdown(f"🤖 **AI:**\n{r}")
    st.markdown("---")