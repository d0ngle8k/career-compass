use axum::{extract::State, http::HeaderMap, Json};

use crate::{
	modules::{
		ai::{models::ChatAssistantRequest, service},
		auth,
	},
	shared::{api_error::ApiError, api_response::ok, app_state::AppState},
};

pub async fn chat_assistant(
	State(state): State<AppState>,
	headers: HeaderMap,
	Json(payload): Json<ChatAssistantRequest>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
	validate_auth(&headers, &state)?;

	if payload.message.trim().len() < 2 {
		return Err(ApiError::BadRequest("Message is too short".to_string()));
	}

	let language = payload.language.as_deref().unwrap_or("vi");
	let result = service::chat_assistant(
		&state,
		payload.message.trim(),
		language,
		payload.jd_text.as_deref(),
		payload.cv_summary.as_deref(),
		payload.history.as_deref(),
	)
	.await?;

	Ok(ok(result))
}

fn validate_auth(headers: &HeaderMap, state: &AppState) -> Result<(), ApiError> {
	let raw = headers
		.get("authorization")
		.and_then(|value| value.to_str().ok())
		.ok_or(ApiError::Unauthorized)?;

	let token = raw.strip_prefix("Bearer ").ok_or(ApiError::Unauthorized)?;
	auth::service::validate_bearer_token(token, state)
}
