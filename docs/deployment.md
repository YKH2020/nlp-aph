# Deployment Guide

This guide provides instructions for setting up and deploying the Autism Parent Helper (APH) application.

## Prerequisites

- Python 3.8+ for the Python implementation
- Rust toolchain for the Rust implementation
- AWS account with appropriate permissions
- Local LLM setup (Llamafile/Zephyr)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nlp-aph
```

### 2. Python Environment Setup

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Rust Environment Setup

```bash
cd rust_scripts
cargo build
cd ..
```

### 4. Environment Variables

Create a `.env` file in the project root with the following variables:

```
KNOWLEDGE_BASE_ID=your-aws-bedrock-knowledge-base-id
```

Configure AWS credentials using one of the standard methods:
- AWS CLI (`aws configure`)
- Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`)
- Credentials file (`~/.aws/credentials`)

### 5. Local LLM Setup

The application expects a local LLM server running with an OpenAI-compatible API:

1. Download a Llamafile-compatible model (e.g., Zephyr)
2. Run the model with the Llamafile server:

```bash
# Example for running a Llamafile model
./zephyr-7b-llamafile.llamafile --server --host 127.0.0.1 --port 8080
```

## Running the Application

### Running the Streamlit Interface

```bash
streamlit run app.py
```

This will start the web interface, typically accessible at http://localhost:8501

### Running from Command Line

#### Python Implementation

```bash
python ./py_scripts/main.py "Your question here"
```

#### Rust Implementation

```bash
./rust_scripts/target/debug/rust_opt "Your question here"
```

## Production Deployment

For production deployment, consider the following options:

### Option 1: AWS EC2 Deployment

1. Launch an EC2 instance with sufficient resources for running the LLM
2. Install dependencies (Python, Rust, etc.)
3. Clone the repository and set up as described above
4. Use a process manager like Supervisor or systemd to keep the application running
5. Set up a reverse proxy (Nginx, Apache) to expose the Streamlit interface

### Option 2: AWS App Runner

For the Streamlit interface without local LLM:

1. Create a Dockerfile for the application
2. Push the Docker image to Amazon ECR
3. Deploy using AWS App Runner
4. Configure the application to use a remotely hosted LLM service

### Option 3: Hybrid Deployment

1. Deploy the LLM on a GPU-enabled EC2 instance
2. Deploy the Streamlit interface on AWS App Runner
3. Configure the Streamlit application to connect to the EC2-hosted LLM

## Monitoring and Maintenance

- Set up CloudWatch monitoring for AWS resources
- Implement logging for application events
- Create regular backups of any persistent data
- Monitor LLM performance and resource usage

## Security Considerations

- Use IAM roles with least privilege for AWS services
- Implement network security groups to restrict access
- Keep dependencies updated
- Consider implementing authentication for the web interface
- Encrypt sensitive data at rest and in transit