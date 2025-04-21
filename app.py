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

# Initialize Streamlit app
st.title("RAG Q&A System")
st.write("Ask a question and get answers from our knowledge base!")

# Set up InferenceClient with Cohere provider
@st.cache_resource
def get_hf_client():
    return InferenceClient(
        provider="cohere",
        api_key=HF_TOKEN,
    )

# Initialize database connection
@st.cache_resource
def init_db():
    return access_db()

def sanitize_prompt(text: str) -> str:
        # Remove control characters *except* newline (\n), carriage return (\r), and tab (\t)
        return re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', text)

# Process query and generate response
def process_query(query):
    db = init_db()
    search_results, final_prompt = create_prompt(db, query, k=5)
    final_prompt = sanitize_prompt(final_prompt)

    client = get_hf_client()
    try:
        completion = client.chat.completions.create(
            model="CohereLabs/aya-expanse-8b",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )
        response = completion.choices[0].message.content

    except Exception as e:
        st.error(f"Error calling inference API: {str(e)}")
        return f"Error: {str(e)}", "", []

    # Get sources
    sources = '\n\n'.join(
        {f"{piece.metadata.get('title', 'Unknown Title')} — {piece.metadata.get('author', 'Unknown Author')}"
         for piece, _ in search_results}
    )

    return response, sources, [score for _, score in search_results]

# Create the user interface
query = st.text_input("Enter your question:")
submit_button = st.button("Submit")

# When user clicks submit
if submit_button and query:
    with st.spinner("Processing your question..."):
        response, sources, relevance_scores = process_query(query)

    st.subheader("Answer:")
    st.write(response)

    with st.expander("View Sources"):
        st.write("This response is based on the following sources:")
        st.write(sources)

    with st.expander("View Relevance Scores"):
        st.write("Relevance scores of retrieved documents:")
        for i, score in enumerate(relevance_scores):
            st.write(f"Document {i+1}: {score:.4f}")

# Sidebar info
st.sidebar.title("About")
st.sidebar.info(
    "This is a RAG (Retrieval-Augmented Generation) Q&A system. "
    "It retrieves relevant information from a knowledge base and "
    "uses the Aya Expanse model via Hugging Face to generate answers based on that context."
)