use axum::{
    extract::{Query, State},
    http::HeaderMap,
    response::{Html, IntoResponse, Redirect, Response},
    Json,
};

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
    headers: HeaderMap,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let (auth_url, csrf_token) = oauth::generate_google_auth_url(&state)?;
    let frontend_url = extract_frontend_url(&headers, &state);
    state.store_oauth_state(csrf_token, frontend_url).await;
    
    Ok(ok(OAuthInitResponse { 
        authorization_url: auth_url 
    }))
}

/// Google OAuth: Step 2 - Handle callback from Google
pub async fn google_callback(
    State(state): State<AppState>,
    Query(params): Query<OAuthCallbackRequest>,
) -> Result<Response, ApiError> {
    let frontend_url = validate_oauth_state(params.state.as_deref(), &state).await?;

    if let Some(provider_error) = params.error.as_deref() {
        let description = params.error_description.as_deref().unwrap_or(provider_error);
        return Ok(build_oauth_error_bridge_response(
            &frontend_url,
            &state.settings.frontend_url,
            description,
        ));
    }

    let code = params
        .code
        .ok_or_else(|| ApiError::BadRequest("Missing authorization code".to_string()))?;

    let user_info = oauth::exchange_google_code(code, &state).await?;
    
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
    let frontend_url = frontend_url.trim_end_matches('/');
    
    Ok(build_oauth_success_bridge_response(
        &frontend_url,
        &state.settings.frontend_url,
        &token,
        &user.email,
    ))
}

/// GitHub OAuth: Step 1 - Redirect user to GitHub consent screen
pub async fn github_login(
    State(state): State<AppState>,
    headers: HeaderMap,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let (auth_url, csrf_token) = oauth::generate_github_auth_url(&state)?;
    let frontend_url = extract_frontend_url(&headers, &state);
    state.store_oauth_state(csrf_token, frontend_url).await;
    
    Ok(ok(OAuthInitResponse { 
        authorization_url: auth_url 
    }))
}

/// GitHub OAuth: Step 2 - Handle callback from GitHub
pub async fn github_callback(
    State(state): State<AppState>,
    Query(params): Query<OAuthCallbackRequest>,
) -> Result<Response, ApiError> {
    let frontend_url = validate_oauth_state(params.state.as_deref(), &state).await?;

    if let Some(provider_error) = params.error.as_deref() {
        let description = params.error_description.as_deref().unwrap_or(provider_error);
        return Ok(build_oauth_error_bridge_response(
            &frontend_url,
            &state.settings.frontend_url,
            description,
        ));
    }

    let code = params
        .code
        .ok_or_else(|| ApiError::BadRequest("Missing authorization code".to_string()))?;

    let user_info = oauth::exchange_github_code(code, &state).await?;
    
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
    
    let frontend_url = frontend_url.trim_end_matches('/');
    
    Ok(build_oauth_success_bridge_response(
        &frontend_url,
        &state.settings.frontend_url,
        &token,
        &user.email,
    ))
}

async fn validate_oauth_state(state_param: Option<&str>, state: &AppState) -> Result<String, ApiError> {
    let token = state_param
        .filter(|value| !value.trim().is_empty())
        .ok_or_else(|| ApiError::BadRequest("Missing OAuth state".to_string()))?;

    if let Some(frontend_url) = state.consume_oauth_state(token).await {
        return Ok(frontend_url);
    }

    Err(ApiError::BadRequest("Invalid or expired OAuth state".to_string()))
}

fn extract_frontend_url(headers: &HeaderMap, state: &AppState) -> String {
    let fallback = state.settings.frontend_url.trim_end_matches('/').to_string();

    headers
        .get("origin")
        .and_then(|v| v.to_str().ok())
        .map(str::trim)
        .filter(|origin| {
            origin.starts_with("http://localhost") || origin.starts_with("http://127.0.0.1")
        })
        .map(|origin| origin.trim_end_matches('/').to_string())
        .unwrap_or(fallback)
}

fn build_oauth_success_bridge_response(
        preferred_frontend: &str,
        fallback_frontend: &str,
        token: &str,
        email: &str,
) -> Response {
        let candidates = oauth_frontend_candidates(preferred_frontend, fallback_frontend);
        let candidates_json = serde_json::to_string(&candidates)
                .unwrap_or_else(|_| "[\"http://localhost:8080\",\"http://localhost:5173\"]".to_string());
        let token_json = serde_json::to_string(token).unwrap_or_else(|_| "\"\"".to_string());
        let email_json = serde_json::to_string(email).unwrap_or_else(|_| "\"\"".to_string());

        let html = format!(
                r#"<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>OAuth Redirect</title>
    </head>
    <body>
        <p>Completing sign-in...</p>
        <script>
            const candidates = {candidates_json};
            const token = {token_json};
            const email = {email_json};

            const withPath = (base, path) => `${{String(base || '').replace(/\/$/, '')}}${{path}}`;

            async function resolveFrontendAndRedirect() {{
                const query = `token=${{encodeURIComponent(token)}}&email=${{encodeURIComponent(email)}}`;
                for (const base of candidates) {{
                    try {{
                        await fetch(withPath(base, '/'), {{ mode: 'no-cors', cache: 'no-store' }});
                        window.location.replace(withPath(base, `/auth/callback?${{query}}`));
                        return;
                    }} catch (_err) {{
                        // Try next candidate
                    }}
                }}

                // Last-resort fallback
                window.location.replace(withPath('http://localhost:8080', `/auth/callback?${{query}}`));
            }}

            resolveFrontendAndRedirect();
        </script>
    </body>
</html>"#
        );

        Html(html).into_response()
}

fn build_oauth_error_bridge_response(
        preferred_frontend: &str,
        fallback_frontend: &str,
        error: &str,
) -> Response {
        let candidates = oauth_frontend_candidates(preferred_frontend, fallback_frontend);
        for base in candidates {
                let redirect_url = format!(
                        "{}/auth?error={}",
                        base.trim_end_matches('/'),
                        urlencoding::encode(error)
                );
                return Redirect::to(&redirect_url).into_response();
        }

        Redirect::to("http://localhost:8080/auth").into_response()
}

fn oauth_frontend_candidates(preferred_frontend: &str, fallback_frontend: &str) -> Vec<String> {
        let mut candidates = Vec::new();

        for url in [
                preferred_frontend,
                fallback_frontend,
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://localhost:5173",
                "http://127.0.0.1:5173",
        ] {
                let normalized = url.trim().trim_end_matches('/');
                if normalized.is_empty() {
                        continue;
                }
                if !candidates.iter().any(|existing| existing == normalized) {
                        candidates.push(normalized.to_string());
                }
        }

        candidates
}
