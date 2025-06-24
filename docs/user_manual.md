# User Manual

This manual provides instructions for using the Autism Parent Helper (APH) application.

## Getting Started

The Autism Parent Helper (APH) is a chatbot designed to provide information, resources, and emotional support to parents of children with autism. It uses a knowledge base built from authoritative sources on autism to provide accurate and helpful responses.

## Using the Web Interface

### Accessing the Application

Once the application is running, access it through your web browser at the provided URL (typically http://localhost:8501 for local deployments).

### Interface Overview

The web interface consists of the following components:

1. **Title Bar**: Displays the application name "🤝 Autism Parent Helper (APH)"
2. **Pipeline Selector**: Radio buttons to choose between Python, Rust, or Both implementations
3. **Chat Input**: A text field at the bottom of the page for entering questions
4. **Chat History**: The main area displaying the conversation history
5. **Performance Metrics**: When using the "Both" option, a table showing performance comparison
6. **Control Buttons**: Buttons to clear chat history and conversation memory

### Asking Questions

1. Select your preferred pipeline (Python, Rust, or Both)
2. Type your question in the chat input field at the bottom of the page
3. Press Enter or click the send button
4. Wait for the response to appear in the chat history

### Pipeline Options

- **🐍 Python**: Uses the Python implementation for processing queries
- **🦀 Rust**: Uses the Rust implementation for processing queries
- **⚖️ Both**: Runs both implementations and displays responses from both for comparison

When using the "Both" option, you'll see performance metrics comparing the response times of the Python and Rust implementations.

### Managing Conversations

- **Clear Chat**: Clears the current chat history from the interface
- **Clear Memory**: Clears the conversation memory (summary) used by the system to maintain context

## Using the Command Line Interface

Both Python and Rust implementations can be used directly from the command line:

### Python CLI

```bash
python ./py_scripts/main.py "Your question here"
```

### Rust CLI

```bash
./rust_scripts/target/debug/rust_opt "Your question here"
```

### Interactive Mode

Running either implementation without a query will start an interactive session:

```bash
python ./py_scripts/main.py
```

In interactive mode:
- Enter your questions when prompted
- Type "exit" or "quit" to end the session

### Clearing Memory

To clear the conversation memory:

```bash
python ./py_scripts/main.py --clear
```

or

```bash
./rust_scripts/target/debug/rust_opt --clear
```

## Example Questions

Here are some example questions you can ask the Autism Parent Helper:

- "How can I help my non-verbal child communicate better?"
- "What are some strategies for managing sensory overload?"
- "How can I explain autism to my child's siblings?"
- "What are some recommended resources for parents of newly diagnosed children?"
- "How can I advocate for my child at school?"

## Troubleshooting

### Common Issues

1. **Slow Responses**: The local LLM may take time to process queries, especially on systems with limited resources
2. **Connection Errors**: Ensure the local LLM server is running and accessible
3. **AWS Errors**: Check AWS credentials and permissions if knowledge retrieval fails

### Getting Help

If you encounter issues not covered in this manual, please:

1. Check the logs for error messages
2. Refer to the technical documentation
3. Contact the project maintainers through the project repository