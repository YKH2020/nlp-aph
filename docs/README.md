# Autism Parent Helper (APH) Documentation

This documentation provides comprehensive information about the Autism Parent Helper (APH) project, a dual-implementation (Python/Rust) RAG (Retrieval Augmented Generation) chatbot designed to assist parents of children with autism.

## Table of Contents

1. [Compliance Documentation](./compliance.md)
2. [Technical Documentation](./technical.md)
3. [API Documentation](./api.md)
4. [Deployment Guide](./deployment.md)
5. [User Manual](./user_manual.md)

## Project Overview

The Autism Parent Helper (APH) is a specialized chatbot that provides information, resources, and emotional support to parents of children with autism. It uses Retrieval Augmented Generation (RAG) to provide accurate, contextually relevant responses based on a curated knowledge base of autism-related literature and resources.

The project features parallel implementations in both Python and Rust, allowing for performance comparison and flexibility in deployment options.

## Key Features

- Dual implementation in Python and Rust
- Retrieval Augmented Generation (RAG) for context-aware responses
- Integration with AWS Bedrock for knowledge retrieval
- Local LLM support via Llamafile/Zephyr
- Streamlit web interface for easy interaction
- Performance comparison between Python and Rust implementations
- Conversation memory and summarization

## Data Sources

The knowledge base is built from several authoritative sources on autism:

- *Sincerely, Your Autistic Child* – Emily Paige Ballou, Sharon daVanport, Morénike Giwa Onaiwu  
- *Plankton Dreams* – Mukhopadhyay  
- *Leaders Around Me* – Edlyn Peña  
- *Communication Alternatives in Autism* – Edlyn Vallejo Peña  
- *Look Me In The Eye* – John Elder Robison  
- *Loud Hands: Autistic People, Speaking* – Julia Bascom  
- *Thinking in Pictures* – Temple Grandin  
- *The Reason I Jump* – Naoki Higashida