use serde::Deserialize;
use serde_json::Value;

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
        let body_text = response
            .text()
            .await
            .unwrap_or_else(|_| "Unable to read response body".to_string());
        return Err(ApiError::Upstream(format_gemini_error(status.as_u16(), &body_text)));
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

fn format_gemini_error(status_code: u16, body_text: &str) -> String {
    if status_code == 429 {
        if let Some(retry_seconds) = extract_retry_delay_seconds(body_text) {
            return format!(
                "Gemini đang quá tải quota. Vui lòng thử lại sau khoảng {} giây.",
                retry_seconds
            );
        }
        return "Gemini đang quá tải quota. Vui lòng thử lại sau khoảng 1 phút.".to_string();
    }

    if let Some(message) = extract_gemini_message(body_text) {
        return format!("Gemini tạm thời không khả dụng ({}).", message);
    }

    format!(
        "Gemini tạm thời không khả dụng (HTTP {}). Vui lòng thử lại sau.",
        status_code
    )
}

fn extract_retry_delay_seconds(body_text: &str) -> Option<u64> {
    let payload: Value = serde_json::from_str(body_text).ok()?;
    let details = payload.get("error")?.get("details")?.as_array()?;

    for detail in details {
        let retry_delay = detail.get("retryDelay")?.as_str()?;
        if let Some(seconds_text) = retry_delay.strip_suffix('s') {
            if let Ok(seconds) = seconds_text.parse::<u64>() {
                return Some(seconds);
            }
        }
    }

    None
}

fn extract_gemini_message(body_text: &str) -> Option<String> {
    let payload: Value = serde_json::from_str(body_text).ok()?;
    let message = payload.get("error")?.get("message")?.as_str()?.trim();
    if message.is_empty() {
        return None;
    }

    // Keep the response concise for user-facing error to avoid exposing raw provider details.
    let first_line = message.lines().next()?.trim();
    if first_line.is_empty() {
        None
    } else {
        Some(first_line.to_string())
    }
}
