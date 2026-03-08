use serde::Deserialize;

use crate::shared::{api_error::ApiError, app_state::AppState};

#[derive(Deserialize)]
struct GeminiResponse {
    candidates: Vec<Candidate>,
}

#[derive(Deserialize)]
struct Candidate {
    content: Content,
}

#[derive(Deserialize)]
struct Content {
    parts: Vec<Part>,
}

#[derive(Deserialize)]
struct Part {
    text: String,
}

pub async fn generate_text(state: &AppState, prompt: String) -> Result<String, ApiError> {
    let url = format!(
        "https://generativelanguage.googleapis.com/v1/models/{}:generateContent?key={}",
        state.settings.gemini_model, state.settings.gemini_api_key
    );

    let body = serde_json::json!({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.5
        }
    });

    let response = state
        .http
        .post(url)
        .json(&body)
        .send()
        .await
        .map_err(|e| ApiError::Upstream(e.to_string()))?;

    if !response.status().is_success() {
        let status = response.status();
        let body_text = response.text().await.unwrap_or_else(|_| "Unable to read response body".to_string());
        return Err(ApiError::Upstream(format!(
            "Gemini error status {}: {}",
            status, body_text
        )));
    }

    let payload: GeminiResponse = response
        .json()
        .await
        .map_err(|e| ApiError::Upstream(e.to_string()))?;

    let text = payload
        .candidates
        .first()
        .and_then(|c| c.content.parts.first())
        .map(|p| p.text.clone())
        .ok_or_else(|| ApiError::Upstream("Gemini returned empty content".to_string()))?;

    Ok(text)
}
