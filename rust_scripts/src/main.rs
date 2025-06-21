mod knowledge_prompt;
mod ollama;

use std::error::Error;
use knowledge_prompt::retrieve_context;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    println!("Your question: ");
    std::io::stdin().read_line(&mut input)?;
    let query = input.trim();

    let context = retrieve_context(query).await?;
    let prompt = format!(
        "Answer the question using the following context:\n\n{}\n\nQuestion: {}",
        context, query
    );

    let response = ollama::ask_ollama("zephyr-7b-beta:latest", &prompt).await?;
    println!("\nResponse:\n{}", response);

    Ok(())
}