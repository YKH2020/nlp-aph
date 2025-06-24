# API Documentation

This document describes the APIs and interfaces used in the Autism Parent Helper (APH) project.

## External APIs

### AWS Bedrock Agent Runtime API

The project uses AWS Bedrock Agent Runtime for knowledge retrieval:

#### Python Implementation

```python
def retrieve_context(query: str) -> str:
    # Initialize the Bedrock Agent Runtime client
    bedrock = boto3.client("bedrock-agent-runtime", region_name="us-east-2")
    knowledge_base_id = os.getenv("KNOWLEDGE_BASE_ID")

    # Retrieve relevant context from the knowledge base
    retrieval_response = bedrock.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": 5}
        },
        retrievalQuery={"text": query}
    )

    # Extract content from the retrieval results
    chunks = [doc["content"]["text"] for doc in retrieval_response["retrievalResults"]]
    context = "\n\n".join(chunks)
    
    return context
```

#### Rust Implementation

```rust
pub async fn retrieve_context(query: &str) -> Result<String, Box<dyn Error>> {
    dotenv().ok();
    let knowledge_base_id = env::var("KNOWLEDGE_BASE_ID")?;

    let config = aws_config::load_defaults(BehaviorVersion::latest()).await;
    let client = Client::new(&config);

    // Construct the retrieval configuration with vector search
    let vector_search_config = KnowledgeBaseVectorSearchConfiguration::builder()
        .number_of_results(5)
        .build();

    let retrieval_config = KnowledgeBaseRetrievalConfiguration::builder()
        .vector_search_configuration(vector_search_config)
        .build();

    // Construct the query
    let retrieval_query = KnowledgeBaseQuery::builder()
        .text(query)
        .build()?;

    // Send retrieve request
    let response = client
        .retrieve()
        .knowledge_base_id(knowledge_base_id)
        .retrieval_configuration(retrieval_config)
        .retrieval_query(retrieval_query)
        .send()
        .await?;

    // Extract content
    let chunks: Vec<String> = response
        .retrieval_results
        .iter()
        .filter_map(|r| r.content().map(|c| c.text().to_string()))
        .collect();
        
    // Join chunks and return
    Ok(chunks.join("\n\n"))
}
```

### Local LLM API (Zephyr)

The project interfaces with a locally running LLM (Zephyr) through an OpenAI-compatible API:

#### Python Implementation

```python
def ask_zephyr(prompt: str, model: str = "APH") -> str:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are APH, an AI assistant. Your top priority is helping "
                    "parents of children with autism with advice, resources, and emotional "
                    "support for helping their child. Always respond with empathy and understanding."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content
```

#### Rust Implementation

```rust
pub async fn ask_zephyr(model: &str, prompt: &str) -> Result<String, Box<dyn Error>> {
    let client = Client::new();
    let request = LlamafileChatRequest {
        model,
        messages: vec![
            ChatMessage {
                role: "system",
                content: "You are APH, an AI assistant. Your top priority is helping parents of children with autism with advice, resources, and emotional support for helping their child. Always respond with empathy and understanding.",
            },
            ChatMessage {
                role: "user",
                content: prompt,
            },
        ],
    };

    let response = client
        .post("http://127.0.0.1:8080/v1/chat/completions")
        .json(&request)
        .send()
        .await?
        .json::<ChatResponse>()
        .await?;

    Ok(response.choices[0].message.content.clone())
}
```

## Internal Functions

### Prompt Formatting

Both implementations use similar functions to format the prompt with context and conversation history:

```python
def format_prompt(summary: str, context: str, query: str) -> str:
    return f"""Chat Summary:
{summary.strip() or '[No prior conversation yet]'}

Retrieved Knowledge:
{context.strip()}

User Query:
{query.strip()}"""
```

### Conversation Management

Both implementations maintain conversation history and provide summarization when the history gets too long:

```python
def update_summary(previous_summary: str, last_user_query: str, last_response: str) -> str:
    return previous_summary + f"\nUser: {last_user_query}\nAPH: {last_response}\n"
```

## CLI Interface

Both implementations provide a command-line interface:

```
# Python
python ./py_scripts/main.py "Your question here"

# Rust
./rust_scripts/target/debug/rust_opt "Your question here"
```

## Web Interface

The Streamlit application provides a web interface with the following features:

- Pipeline selection (Python, Rust, or Both)
- Chat input
- Response display
- Performance metrics
- Chat history management
- Memory clearing