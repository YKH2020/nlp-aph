mod zephyr;
mod knowledge_prompt;

use std::error::Error;
use std::io::{self, Write};
use zephyr::ask_zephyr;
use knowledge_prompt::retrieve_context;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    print!("Your question: ");
    io::stdout().flush()?;

    let mut input = String::new();
    io::stdin().read_line(&mut input)?;
    let query = input.trim();

    // 🧠 Retrieve context from AWS KB
    let context = retrieve_context(query).await?;

    // 💬 Format prompt with context
    let prompt = format!(
        "Answer the question using the following context:\n\n{}\n\nQuestion: {}",
        context, query
    );

    // 🔁 Ask Llamafile (zephyr model)
    let response = ask_zephyr("APH", &prompt).await?;
    println!("\nResponse:\n{}", response);

    Ok(())
}