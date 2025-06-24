import os
import boto3
from dotenv import load_dotenv
load_dotenv()

def retrieve_context(query: str) -> str:
    """
    Retrieve relevant context from an AWS Knowledge Base using the Bedrock Agent Runtime API.
    
    Args:
        query (str): The user's query to search for relevant context.
    
    Returns:
        str: The retrieved context as a string.
    """
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

    # print(f"Retrieved {len(chunks)} chunks.")
    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i+1}: {chunk[:50]}...")

    context = "\n\n".join(chunks)
    
    return context