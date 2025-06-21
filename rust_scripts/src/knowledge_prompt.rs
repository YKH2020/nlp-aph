use aws_config::BehaviorVersion;
use aws_sdk_bedrockagentruntime::{
    Client,
    types::{
        KnowledgeBaseQuery,
        KnowledgeBaseRetrievalConfiguration,
        KnowledgeBaseVectorSearchConfiguration,
    },
};
use std::error::Error;

pub async fn retrieve_context(query: &str) -> Result<String, Box<dyn Error>> {
    let config = aws_config::load_defaults(BehaviorVersion::latest()).await;
    let client = Client::new(&config);

    // Construct the retrieval configuration with vector search
    let vector_search_config = KnowledgeBaseVectorSearchConfiguration::builder()
        .number_of_results(10)
        .build();

    let retrieval_config = KnowledgeBaseRetrievalConfiguration::builder()
        .vector_search_configuration(vector_search_config)
        .build();

    // Construct the query
    let retrieval_query = KnowledgeBaseQuery::builder()
        .text(query)
        .build()?; // propagate error

    // Send retrieve request
    let response = client
        .retrieve()
        .knowledge_base_id("EKJ8WM0BAW")
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

    println!("Retrieved {} chunks.", chunks.len());
    for (i, chunk) in chunks.iter().enumerate() {
        println!("Chunk {}: {}...", i + 1, &chunk[..chunk.len().min(50)]);
    }

    Ok(chunks.join("\n\n"))
}
