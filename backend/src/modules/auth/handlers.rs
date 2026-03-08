use axum::{extract::State, http::HeaderMap, Json};

use crate::{
    modules::auth::{
        models::{LoginRequest, LoginResponse, LogoutResponse, RegisterRequest, RegisterResponse},
        service,
    },
    shared::{api_error::ApiError, api_response::ok, app_state::AppState},
};

pub async fn register(
    State(state): State<AppState>,
    Json(payload): Json<RegisterRequest>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let email = payload.email.trim().to_lowercase();
    service::register(&email, payload.password.trim(), &state)?;

    Ok(ok(RegisterResponse {
        message: "Registered successfully",
        email,
    }))
}

pub async fn login(
    State(state): State<AppState>,
    Json(payload): Json<LoginRequest>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let email = payload.email.trim().to_lowercase();
    service::validate_credentials(&email, payload.password.trim(), &state)?;
    let token = service::login(&email, &state)?;

    Ok(ok(LoginResponse {
        access_token: token,
        token_type: "Bearer",
        expires_in_minutes: state.settings.jwt_expires_minutes,
    }))
}

pub async fn logout(
    State(state): State<AppState>,
    headers: HeaderMap,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let token = extract_bearer(&headers)?;
    service::validate_bearer_token(&token, &state)?;
    Ok(ok(LogoutResponse {
        message: "Logged out successfully",
    }))
}

fn extract_bearer(headers: &HeaderMap) -> Result<String, ApiError> {
    let raw = headers
        .get("authorization")
        .and_then(|value| value.to_str().ok())
        .ok_or(ApiError::Unauthorized)?;

    if let Some(token) = raw.strip_prefix("Bearer ") {
        Ok(token.to_string())
    } else {
        Err(ApiError::Unauthorized)
    }
}
