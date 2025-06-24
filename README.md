# Autism Parent Helper (RAG Chatbot)

A dual-implementation (Python/Rust) RAG chatbot designed to provide support, resources, and information to parents of children with autism.

## Description

Parents of children diagnosed with autism often face confusion about their child's condition, especially with nonverbal children—how do I help them communicate? Are there better strategies for gauging their learning? These questions are rarely answered, with minimal tools that directly educate parents of both verbal and nonverbal special needs children. Although tools and datasets exist to support speech and early autism detection, a comprehensive educational solution remains lacking.

This project implements a Retrieval Augmented Generation (RAG) chatbot in both Python and Rust, allowing for performance comparison while providing valuable information to parents.

## Features

- Dual implementation in Python and Rust
- Retrieval Augmented Generation (RAG) using AWS Bedrock
- Local LLM support via Llamafile/Zephyr
- Streamlit web interface
- Performance comparison between implementations
- Conversation memory and summarization

## Data Sources

Lived experiences and firsthand accounts are of paramount importance. This project draws insights from such information, specifically through the following sources:
- *Sincerely, Your Autistic Child* – Emily Paige Ballou, Sharon daVanport, Morénike Giwa Onaiwu  
- *Plankton Dreams* – Mukhopadhyay  
- *Leaders Around Me* – Edlyn Peña  
- *Communication Alternatives in Autism* – Edlyn Vallejo Peña  
- *Look Me In The Eye* – John Elder Robison  
- *Loud Hands: Autistic People, Speaking* – Julia Bascom  
- *Thinking in Pictures* – Temple Grandin  
- *The Reason I Jump* – Naoki Higashida

## Documentation

Comprehensive documentation is available in the [docs](./docs) directory:

- [Technical Documentation](./docs/technical.md)
- [API Documentation](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)
- [User Manual](./docs/user_manual.md)
- [Compliance Documentation](./docs/compliance.md)
- [Development Environment Setup](./docs/development_environment.md)

## Quick Start

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   cd rust_scripts && cargo build && cd ..
   ```
3. Set up environment variables in `.env`:
   ```
   KNOWLEDGE_BASE_ID=your-aws-bedrock-knowledge-base-id
   ```
4. Start a local LLM server (Llamafile/Zephyr)
5. Run the Streamlit interface:
   ```
   streamlit run app.py
   ```
# [Video Presentation](https://youtu.be/oZWAXjmXgz0)
## Future Work

- Explore sentence clustering / non-DL / naive approaches for data cleaning / organization
- Shift to a different deployment platform (AWS EC2 / AppRunner and deal with cost) / migrate to a blog website
- Curate better ground truth from parents for testing and evaluation