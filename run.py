import streamlit as st
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

from scripts.access_db import access_db
from scripts.create_prompt import create_prompt

# Load Hugging Face token from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize Hugging Face Inference Client (exact config you used)
def load_hf_client():
    return InferenceClient(
        provider="cohere",
        api_key=HF_TOKEN,
    )

# Use HF client to generate a response
def query_aya():
    client = load_hf_client()

    completion = client.chat.completions.create(
        model="CohereLabs/aya-expanse-8b",
        messages=[
            {
                "role": "user", 
                "content": "What's the difference between aspergers and autism?"
            }
        ],
    )

    return completion.choices[0].message

print(query_aya())

