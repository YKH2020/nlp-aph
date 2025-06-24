mod zephyr;
mod knowledge_prompt;

use std::env;
use std::error::Error;
use std::fs;
use std::io::{self, Write};
use zephyr::ask_zephyr;
use knowledge_prompt::retrieve_context;

const SUMMARY_PATH: &str = ".summary.txt";

fn clean_response(text: &str) -> String {
    // Remove trailing </s> and trim surrounding whitespace
    text.trim_end_matches("</s>").trim().to_string()
}

fn load_summary() -> String {
    fs::read_to_string(SUMMARY_PATH).unwrap_or_default()
}

fn save_summary(summary: &str) {
    let _ = fs::write(SUMMARY_PATH, summary);
}

fn update_summary(summary: &str, user: &str, response: &str) -> String {
    format!("{}\nUser: {}\nAPH: {}\n", summary, user, response)
}

fn format_prompt(summary: &str, context: &str, query: &str) -> String {
    format!(
        "Chat Summary:\n{}\n\nRetrieved Knowledge:\n{}\n\nUser Query:\n{}",
        if summary.trim().is_empty() {
            "[No prior conversation yet]"
        } else {
            summary.trim()
        },
        context.trim(),
        query.trim()
    )
}

async fn condense_summary(full_summary: &str) -> Result<String, Box<dyn Error>> {
    let summarization_prompt = format!(
        "Summarize this conversation in 2–3 sentences:\n\n{}",
        full_summary
    );

    let raw = ask_zephyr("APH", &summarization_prompt).await?;
    let cleaned = clean_response(&raw);
    Ok(cleaned)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();

    // 🧹 Clear memory
    if args.len() == 2 && args[1] == "--clear" {
        save_summary("");
        println!("Chat summary cleared.");
        return Ok(());
    }

    if args.len() > 1 {
        // 🚀 CLI mode
        let query = args[1..].join(" ");
        let mut chat_summary = load_summary();

        let context = retrieve_context(&query).await?;
        let prompt = format_prompt(&chat_summary, &context, &query);

        let response = ask_zephyr("APH", &prompt).await?;
        let cleaned = clean_response(&response);
        println!("{}", cleaned);

        chat_summary = update_summary(chat_summary.as_str(), query.as_str(), cleaned.as_str());

        if chat_summary.lines().count() > 3 {
            chat_summary = condense_summary(&chat_summary).await?;
        }

        save_summary(&chat_summary);
    } else {
        // 🖥️ Interactive mode
        let mut chat_summary = load_summary();

        loop {
            print!("Your question (or 'exit'): ");
            io::stdout().flush()?;

            let mut input = String::new();
            io::stdin().read_line(&mut input)?;
            let query = input.trim();

            if query.eq_ignore_ascii_case("exit") || query.eq_ignore_ascii_case("quit") {
                break;
            }

            let context = retrieve_context(query).await?;
            let prompt = format_prompt(&chat_summary, &context, query);

            let response = ask_zephyr("APH", &prompt).await?;
            println!("{}", response);

            chat_summary = update_summary(&chat_summary, &query, &response);

            if chat_summary.lines().count() > 3 {
                chat_summary = condense_summary(&chat_summary).await?;
            }

            save_summary(&chat_summary);
        }
    }

    Ok(())
}