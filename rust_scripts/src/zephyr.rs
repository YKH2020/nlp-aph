use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::error::Error;

#[derive(Serialize)]
struct ChatMessage<'a> {
    role: &'a str,
    content: &'a str,
}

#[derive(Serialize)]
struct LlamafileChatRequest<'a> {
    model: &'a str,
    messages: Vec<ChatMessage<'a>>,
}

#[derive(Deserialize)]
struct ChatResponse {
    choices: Vec<ChatChoice>,
}

#[derive(Deserialize)]
struct ChatChoice {
    message: ChatMessageOwned,
}

#[derive(Deserialize)]
struct ChatMessageOwned {
    role: String,
    content: String,
}

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
        .header("Authorization", "Bearer no-key")
        .json(&request)
        .send()
        .await?;

    let parsed: ChatResponse = response.json().await?;
    let content = parsed
        .choices
        .first()
        .map(|c| c.message.content.clone())
        .unwrap_or_else(|| "No response.".to_string());

    Ok(content)
}