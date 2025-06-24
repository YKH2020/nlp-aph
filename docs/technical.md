# Technical Documentation

This document provides technical details about the Autism Parent Helper (APH) project architecture, components, and implementation.

## Architecture Overview

The APH project is implemented in both Python and Rust with identical functionality, allowing for performance comparison. The architecture follows a Retrieval Augmented Generation (RAG) pattern:

1. **User Query Processing**: The user submits a question through the Streamlit interface
2. **Knowledge Retrieval**: The query is sent to AWS Bedrock to retrieve relevant context from the knowledge base
3. **Context Augmentation**: The retrieved context is combined with the user query and conversation history
4. **Response Generation**: The augmented prompt is sent to a local LLM (Zephyr) for response generation
5. **Conversation Management**: The conversation history is updated and summarized as needed

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  User Query  │────▶│  Knowledge  │────▶│  Response   │
│             │     │  Retrieval  │     │ Generation  │
└─────────────┘     └─────────────┘     └─────────────┘
                          │                    │
                          ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │ Conversation│◀────│   Output    │
                    │   Memory    │     │  to User    │
                    └─────────────┘     └─────────────┘
```

## Components

### Python Implementation

- **knowledge_prompt.py**: Handles retrieval from AWS Bedrock knowledge base
- **zephyr.py**: Interfaces with the local LLM (Zephyr) via OpenAI-compatible API
- **main.py**: Orchestrates the workflow and manages conversation history

### Rust Implementation

- **knowledge_prompt.rs**: Rust equivalent for AWS Bedrock knowledge retrieval
- **zephyr.rs**: Rust implementation of the LLM interface
- **main.rs**: Main workflow orchestration in Rust

### Web Interface

- **app.py**: Streamlit application that provides the user interface and allows switching between Python and Rust implementations

## Dependencies

### Python Dependencies

```
boto3                # AWS SDK for Python
openai               # OpenAI client for local LLM interface
python-dotenv        # Environment variable management
streamlit            # Web interface
pandas               # Data handling for performance metrics
```

### Rust Dependencies

```
tokio                # Async runtime
reqwest              # HTTP client
serde                # Serialization/deserialization
aws-config           # AWS configuration
aws-sdk-bedrockagentruntime  # AWS Bedrock client
dotenvy              # Environment variable management
```

## Data Flow

1. User submits a query through the Streamlit interface
2. Based on the selected pipeline (Python, Rust, or Both), the query is processed
3. The system retrieves relevant context from AWS Bedrock knowledge base
4. The context is combined with the query and conversation history
5. The augmented prompt is sent to the local LLM
6. The response is displayed to the user
7. Conversation history is updated and summarized if needed

## Configuration

The application uses environment variables for configuration:

- `KNOWLEDGE_BASE_ID`: ID of the AWS Bedrock knowledge base
- AWS credentials are managed through the standard AWS SDK configuration

## Performance Considerations

The dual implementation allows for performance comparison between Python and Rust. The Streamlit interface includes performance logging to track response times for each implementation.