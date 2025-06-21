use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::error::Error;

#[derive(Serialize)]
struct OllamaRequest<'a> {
    model: &'a str,
    prompt: &'a str,
}

#[derive(Deserialize)]
struct OllamaResponse {
    response: String,
}

pub async fn ask_ollama(model: &str, prompt: &str) -> Result<String, Box<dyn Error>> {
    let client = Client::new();
    let res = client
        .post("http://172.31.112.1:11434/api/generate")
        .json(&OllamaRequest { model, prompt })
        .send()
        .await?;

    let json: OllamaResponse = res.json().await?;
    Ok(json.response)
}