import streamlit as st
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

from scripts.access_db import access_db
from scripts.create_prompt import create_prompt

# Load Hugging Face token from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def load_hf_client():
    return InferenceClient(
        provider="cohere",
        api_key=HF_TOKEN,
    )

def query_aya(prompt: str):
    client = load_hf_client()

    completion = client.chat.completions.create(
        model="CohereLabs/aya-expanse-8b",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
    )

    return completion.choices[0].message.content

# --- Streamlit UI ---
st.set_page_config(page_title="Autism Support Chatbot")
st.title("🧠 Autism Support Chatbot")

query = st.text_input("Ask a question about autism:")

if query:
    with st.spinner("🔍 Searching sources..."):
        db = access_db()
        search_results, final_prompt = create_prompt(db, query)

    with st.spinner("💬 Generating response..."):
        response = query_aya(final_prompt)

    st.markdown("### ✅ Answer")
    st.markdown(response.strip())

    st.markdown("### 📚 Sources")
    for doc, _ in search_results:
        title = doc.metadata.get("title", "Unknown Title")
        author = doc.metadata.get("author", "Unknown Author")
        st.markdown(f"- **{title}** by *{author}*")