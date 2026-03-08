use axum::{extract::{Query, State}, http::HeaderMap, response::Redirect, Json};

use crate::{
    modules::auth::{
        models::{AuthProvider, LoginRequest, LoginResponse, LogoutResponse, OAuthCallbackRequest, OAuthInitResponse, RegisterRequest, RegisterResponse},
        oauth, service,
    },
    shared::{api_error::ApiError, api_response::ok, app_state::AppState},
};

pub async fn register(
    State(state): State<AppState>,
    Json(payload): Json<RegisterRequest>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let email = payload.email.trim().to_lowercase();
    service::register(&email, payload.password.trim(), &state).await?;

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
    service::validate_credentials(&email, payload.password.trim(), &state).await?;
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

// ==================== OAuth Handlers ====================

/// Google OAuth: Step 1 - Redirect user to Google consent screen
pub async fn google_login(
    State(state): State<AppState>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let (auth_url, _csrf_token) = oauth::generate_google_auth_url(&state)?;
    
    // TODO: Store csrf_token in session/cache for verification
    // For now, we skip CSRF validation for simplicity
    
    Ok(ok(OAuthInitResponse { 
        authorization_url: auth_url 
    }))
}

/// Google OAuth: Step 2 - Handle callback from Google
pub async fn google_callback(
    State(state): State<AppState>,
    Query(params): Query<OAuthCallbackRequest>,
) -> Result<Redirect, ApiError> {
    // TODO: Verify CSRF token from state parameter
    
    let user_info = oauth::exchange_google_code(params.code, &state).await?;
    
    // Find or create user in database
    let user = service::find_or_create_oauth_user(
        &user_info.email,
        user_info.name.as_deref(),
        user_info.picture.as_deref(),
        &user_info.id,
        AuthProvider::Google,
        &state,
    ).await?;
    
    // Generate JWT token
    let token = service::login(&user.email, &state)?;
    
    // Redirect to frontend with token
    let frontend_url = state.settings.frontend_url.trim_end_matches('/');
    let redirect_url = format!(
        "{}/auth/callback?token={}&email={}",
        frontend_url,
        token,
        urlencoding::encode(&user.email)
    );
    
    Ok(Redirect::to(&redirect_url))
}

/// GitHub OAuth: Step 1 - Redirect user to GitHub consent screen
pub async fn github_login(
    State(state): State<AppState>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let (auth_url, _csrf_token) = oauth::generate_github_auth_url(&state)?;
    
    Ok(ok(OAuthInitResponse { 
        authorization_url: auth_url 
    }))
}

/// GitHub OAuth: Step 2 - Handle callback from GitHub
pub async fn github_callback(
    State(state): State<AppState>,
    Query(params): Query<OAuthCallbackRequest>,
) -> Result<Redirect, ApiError> {
    let user_info = oauth::exchange_github_code(params.code, &state).await?;
    
    // GitHub users can hide their email, use login as fallback
    let email = user_info.email
        .unwrap_or_else(|| format!("{}@github.local", user_info.login));
    
    let user = service::find_or_create_oauth_user(
        &email,
        user_info.name.as_deref(),
        user_info.avatar_url.as_deref(),
        &user_info.id.to_string(),
        AuthProvider::GitHub,
        &state,
    ).await?;
    
    let token = service::login(&user.email, &state)?;
    
    let frontend_url = state.settings.frontend_url.trim_end_matches('/');
    let redirect_url = format!(
        "{}/auth/callback?token={}&email={}",
        frontend_url,
        token,
        urlencoding::encode(&user.email)
    );
    
    Ok(Redirect::to(&redirect_url))
}
