# Development Environment Setup Guide

This guide provides detailed instructions for setting up a development environment for the Autism Parent Helper (APH) project.

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **CPU**: 4+ cores recommended (especially for running local LLMs)
- **RAM**: 16GB+ recommended (8GB minimum)
- **Storage**: 10GB+ free space
- **GPU**: Optional but recommended for faster LLM inference

## Software Prerequisites

### Required Software

1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure pip is installed and updated

2. **Rust Toolchain**
   - Install using [rustup](https://rustup.rs/)
   - Includes Cargo package manager

3. **Git**
   - Download from [git-scm.com](https://git-scm.com/downloads)

4. **AWS CLI**
   - Install following [AWS documentation](https://aws.amazon.com/cli/)
   - Configure with appropriate credentials

### Optional Software

1. **Visual Studio Code** or other IDE
   - Recommended extensions:
     - Python
     - Rust-analyzer
     - Even Better TOML
     - GitLens

2. **Docker** (for containerized deployment testing)

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd nlp-aph
```

### 2. Python Environment Setup

```bash
# Create and activate a virtual environment
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

### 4. Environment Configuration

Create a `.env` file in the project root:

```
KNOWLEDGE_BASE_ID=your-aws-bedrock-knowledge-base-id
```

### 5. Local LLM Setup

For local development, you'll need a running LLM server:

1. Download a Llamafile-compatible model (e.g., Zephyr)
2. Run the model with the Llamafile server:

```bash
# Example for running a Llamafile model
./zephyr-7b-llamafile.llamafile
```
OR
```bash
# Default config
./zephyr-7b-llamafile.llamafile --server --host 127.0.0.1 --port 8080
```
OR
```bash
# Running with a GPU (HIGHLY RECOMMENDED)
./zephyr-7b-llamafile.llamafile -ngl 30 --gpu nvidia
```
## AWS Setup

### 1. Create a Knowledge Base in AWS Bedrock

1. Log in to the AWS Management Console
2. Navigate to Amazon Bedrock
3. Create a Knowledge Base:
   - Select a vector store
   - Configure data sources
   - Set up embedding model
   - Note the Knowledge Base ID for your `.env` file

### 2. Configure AWS Credentials

Set up AWS credentials using one of these methods:

- AWS CLI: `aws configure`
- Environment variables:
  ```
  AWS_ACCESS_KEY_ID=your-access-key
  AWS_SECRET_ACCESS_KEY=your-secret-key
  AWS_REGION=us-east-2
  ```
- Credentials file: `~/.aws/credentials`

### 3. IAM Permissions

Ensure your AWS user/role has these permissions:

- `bedrock:InvokeModel`
- `bedrock-agent-runtime:Retrieve`
- Related S3 permissions if using S3 for knowledge base storage

## Running the Application

### Start the Streamlit Interface

```bash
streamlit run app.py
```

### Run the Python Implementation

```bash
python ./py_scripts/main.py "Your test query"
```

### Run the Rust Implementation

```bash
./rust_scripts/target/debug/rust_opt "Your test query"
```

## Development Workflow

### Code Organization

- `py_scripts/`: Python implementation
- `rust_scripts/`: Rust implementation
- `app.py`: Streamlit web interface
- `data/`: Knowledge base data
- `deprecated/`: Legacy code (for reference)

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make changes to the code
3. Test changes locally
4. Commit changes: `git commit -am "Description of changes"`
5. Push to remote: `git push origin feature/your-feature-name`

### Testing

- Test both Python and Rust implementations
- Compare performance metrics
- Verify AWS integration
- Test the web interface

## Troubleshooting

### Common Development Issues

1. **AWS Connectivity Issues**
   - Verify AWS credentials
   - Check region configuration
   - Ensure proper IAM permissions

2. **Local LLM Issues**
   - Verify the LLM server is running
   - Check port configuration (default: 8080)
   - Ensure sufficient system resources

3. **Rust Build Errors**
   - Update Rust toolchain: `rustup update`
   - Check dependencies in Cargo.toml
   - Clear cargo cache if needed: `cargo clean`

4. **Python Import Errors**
   - Verify virtual environment is activated
   - Check installed packages: `pip list`
   - Install missing dependencies: `pip install -r requirements.txt`