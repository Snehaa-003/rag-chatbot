"""
streamlit_app.py
-----------------
A simple, clean web UI for your RAG chatbot using Streamlit.

Run with:
    streamlit run streamlit_app.py

This will open a browser tab with a chat interface. Same underlying pipeline
as app.py (chatbot.py) — this is just a nicer way to interact with it and demo it.
"""

import streamlit as st
from chatbot import answer_question

st.set_page_config(
    page_title="DecodeWher — DSA Bot",
    page_icon="🔓",
    layout="centered",
)

# ---------- Custom theme: "decode" aesthetic tied to @decodewher ----------
# Deep violet-to-ink gradient background, electric violet + hot pink accents,
# Space Grotesk for display type, Inter for body, JetBrains Mono for code.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@500&display=swap');

.stApp {
    background: linear-gradient(160deg, #12091f 0%, #1b0f33 45%, #150a28 100%);
    font-family: 'Inter', sans-serif;
}

/* Hero title block */
.decode-hero {
    text-align: left;
    margin-bottom: 0.25rem;
}
.decode-hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.2rem;
    background: linear-gradient(90deg, #C084FC, #F472B6 60%, #FB923C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.decode-hero p {
    color: #B8AEDB;
    font-size: 0.95rem;
    margin-top: 0.15rem;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 0.4rem 0.2rem;
}
[data-testid="stChatMessageContent"] {
    font-family: 'Inter', sans-serif;
}

/* User messages: solid gradient pill */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(120deg, #8B5CF6, #EC4899);
    border-radius: 18px 18px 4px 18px;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p {
    color: white !important;
}

/* Assistant messages: glassy dark card */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(196, 132, 252, 0.25);
    border-radius: 18px 18px 18px 4px;
}

/* Code snippets inside answers, in mono */
[data-testid="stChatMessageContent"] code {
    font-family: 'JetBrains Mono', monospace;
    background: rgba(196, 132, 252, 0.15);
    color: #F472B6;
    border-radius: 4px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.02);
    border-right: 1px solid rgba(196, 132, 252, 0.15);
}
[data-testid="stSidebar"] h2 {
    font-family: 'Space Grotesk', sans-serif;
    color: #F472B6;
}

/* Chat input box */
[data-testid="stChatInput"] textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(196, 132, 252, 0.3) !important;
    border-radius: 14px !important;
    color: #F5F3FF !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(120deg, #8B5CF6, #EC4899);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Space Grotesk', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="decode-hero">
    <h1>🔓 DecodeWher DSA Bot</h1>
    <p>Ask anything from the notes — answers pulled straight from what's actually been taught.</p>
</div>
""", unsafe_allow_html=True)

BOT_AVATAR = "🔓"
USER_AVATAR = "🎯"

# Keep chat history across reruns using Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for msg in st.session_state.messages:
    avatar = BOT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(f"📎 {', '.join(msg['sources'])}")

# Chat input box at the bottom
question = st.chat_input("Ask a DSA question...")

if question:
    # Show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(question)

    # Get the answer and show it with a loading spinner
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner("🔓 Decoding..."):
            answer, sources = answer_question(question)
        st.markdown(answer)
        if sources:
            st.caption(f"📎 {', '.join(sources)}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

# Sidebar with a reset button and quick info
with st.sidebar:
    st.header("✨ About")
    st.write(
        "Ask questions about DSA topics covered in the notes. "
        "Answers stay grounded in what's actually been taught — "
        "no made-up explanations."
    )
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()