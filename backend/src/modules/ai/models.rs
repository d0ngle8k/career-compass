use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct ChatMessage {
    pub role: String,
    pub content: String,
}

#[derive(Deserialize)]
pub struct ChatAssistantRequest {
    pub message: String,
    pub language: Option<String>,
    pub jd_text: Option<String>,
    pub cv_summary: Option<String>,
    pub history: Option<Vec<ChatMessage>>,
}

#[derive(Serialize, Deserialize)]
pub struct ChatAssistantResponse {
    pub reply: String,
}
