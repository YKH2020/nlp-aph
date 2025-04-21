import streamlit as st
from huggingface_hub import InferenceClient
from scripts.create_prompt import create_prompt
from scripts.access_db import access_db
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Page config
st.set_page_config(page_title="Autism Parent Helper", layout="wide")

# Sidebar
st.sidebar.markdown("""
This is a **Retrieval-Augmented Generation** (RAG) system powered by the **Aya Expanse 8B** model via Hugging Face.

It provides helpful answers sourced from trusted documents to assist parents navigating autism-related topics.

_Improvements coming soon!_
""")

# Init chat state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Cache: inference + DB
@st.cache_resource
def get_hf_client():
    return InferenceClient(provider="cohere", api_key=HF_TOKEN)

@st.cache_resource
def init_db():
    return access_db()

# Clean prompt
def sanitize_prompt(text: str) -> str:
    return re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', text)

# Generate response
def process_query(query):
    db = init_db()
    search_results, final_prompt = create_prompt(db, query, k=5)
    final_prompt = sanitize_prompt(final_prompt)

    client = get_hf_client()
    try:
        completion = client.chat.completions.create(
            model="CohereLabs/aya-expanse-8b",
            messages=[
                {"role": "user", "content": final_prompt}
            ]
        )
        response = completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling inference API: {str(e)}")
        return f"Error: {str(e)}", "", []

    sources = '\n\n'.join({
        f"{piece.metadata.get('title', 'Unknown Title')} — {piece.metadata.get('author', 'Unknown Author')}"
        for piece, _ in search_results
    })
    relevance_scores = [score for _, score in search_results]

    return response, sources, relevance_scores

# App title
st.title("🤝 Autism Parent Helper (APH)")

# Input bar
query = st.chat_input("Ask a question about autism, parenting, or support...")

# Trigger a new response
if query:
    with st.spinner("Thinking..."):
        response, sources, scores = process_query(query)
    st.session_state.chat_history.append({
        "query": query,
        "response": response,
        "sources": sources,
        "scores": scores
    })
    st.rerun()  # Force refresh to show new output immediately

# Show chat messages
for entry in st.session_state.chat_history:
    with st.chat_message("user", avatar="❓"):
        st.markdown(entry["query"])
    with st.chat_message("assistant", avatar="🤗"):
        st.markdown(entry["response"])
        with st.expander("📖 Sources"):
            st.markdown(entry["sources"] or "No sources found.")
        with st.expander("📈 Relevance Scores"):
            for i, score in enumerate(entry["scores"]):
                st.write(f"Document {i+1}: {score:.4f}")

# Centered clear button
st.markdown("---")
clear_btn = st.button("🔌 Clear Chat", use_container_width=True)
if clear_btn:
    st.session_state.chat_history = []
    st.rerun()