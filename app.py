import asyncio
import streamlit as st
from agent.agent_graph import build_agent, chat_with_memory

st.set_page_config(page_title="Personal Ops Agent", page_icon="🤖")
st.title("🤖 Personal Ops Agent")
st.caption("An AI agent with memory, connected to your Task Manager and GitHub via MCP")


@st.cache_resource
def get_agent():
    """
    Builds the agent ONCE and caches it across reruns —
    otherwise Streamlit would relaunch both MCP server subprocesses
    every single time you send a message.
    """
    return asyncio.run(build_agent())


agent = get_agent()

# Keep chat history in Streamlit's session state (persists during this browser tab session)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box at the bottom
user_input = st.chat_input("Ask me to manage tasks or check GitHub issues...")

if user_input:
    # Show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run the agent (async function called from sync Streamlit code)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = asyncio.run(chat_with_memory(agent, user_input))
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})