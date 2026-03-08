use serde::{Deserialize, Serialize};
use std::time::Duration;

use crate::{
    modules::scoring::models::ScoreCvResponse,
    shared::{api_error::ApiError, app_state::AppState},
};

#[derive(Serialize)]
struct NlpScoreRequest<'a> {
    cv_text: &'a str,
    jd_text: &'a str,
    language: &'a str,
}

#[derive(Deserialize)]
struct NlpScoreEnvelope {
    success: bool,
    data: Option<ScoreCvResponse>,
    error: Option<String>,
}

pub async fn score_cv(
    state: &AppState,
    cv_text: &str,
    jd_text: &str,
    language: &str,
) -> Result<ScoreCvResponse, ApiError> {
    let url = format!("{}/score-cv", state.settings.nlp_service_url.trim_end_matches('/'));
    let request = NlpScoreRequest {
        cv_text,
        jd_text,
        language,
    };

    let response = state
        .http
        .post(url)
        .timeout(Duration::from_millis(state.settings.nlp_timeout_ms))
        .json(&request)
        .send()
        .await
        .map_err(|e| ApiError::Upstream(format!("NLP service unavailable: {e}")))?;

    let status = response.status();
    let body = response
        .text()
        .await
        .map_err(|e| ApiError::Upstream(format!("Failed to read NLP response: {e}")))?;

    if !status.is_success() {
        return Err(ApiError::Upstream(format!(
            "NLP service status {}: {}",
            status, body
        )));
    }

    let envelope: NlpScoreEnvelope = serde_json::from_str(&body).map_err(|e| {
        ApiError::Upstream(format!(
            "Failed to parse NLP response JSON: {e}. Raw body: {body}"
        ))
    })?;

    if !envelope.success {
        let message = envelope
            .error
            .unwrap_or_else(|| "NLP service returned unsuccessful result".to_string());
        return Err(ApiError::Upstream(message));
    }

    envelope
        .data
        .ok_or_else(|| ApiError::Upstream("NLP response missing data payload".to_string()))
}
