use oauth2::{
    AuthUrl, AuthorizationCode, ClientId, ClientSecret, CsrfToken,
    RedirectUrl, Scope, TokenResponse, TokenUrl,
    AuthType,
    basic::BasicClient,
    reqwest::async_http_client,
};
use serde::Deserialize;
use crate::shared::{api_error::ApiError, app_state::AppState};

// Google OAuth URLs
const GOOGLE_AUTH_URL: &str = "https://accounts.google.com/o/oauth2/v2/auth";
const GOOGLE_TOKEN_URL: &str = "https://oauth2.googleapis.com/token";
const GOOGLE_USERINFO_URL: &str = "https://www.googleapis.com/oauth2/v2/userinfo";

// GitHub OAuth URLs
const GITHUB_AUTH_URL: &str = "https://github.com/login/oauth/authorize";
const GITHUB_TOKEN_URL: &str = "https://github.com/login/oauth/access_token";
const GITHUB_USER_URL: &str = "https://api.github.com/user";
const GITHUB_EMAIL_URL: &str = "https://api.github.com/user/emails";

#[derive(Debug, Deserialize)]
pub struct GoogleUserInfo {
    pub id: String,
    pub email: String,
    pub name: Option<String>,
    pub picture: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct GitHubUserInfo {
    pub id: u64,
    pub email: Option<String>,
    pub login: String,
    pub name: Option<String>,
    pub avatar_url: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct GitHubEmail {
    pub email: String,
    pub primary: bool,
    pub verified: bool,
}

pub fn create_google_client(state: &AppState) -> Result<BasicClient, ApiError> {
    if state.settings.google_client_id.is_empty() {
        return Err(ApiError::BadRequest("Google OAuth not configured".to_string()));
    }

    Ok(BasicClient::new(
        ClientId::new(state.settings.google_client_id.clone()),
        Some(ClientSecret::new(state.settings.google_client_secret.clone())),
        AuthUrl::new(GOOGLE_AUTH_URL.to_string()).map_err(|_| ApiError::Internal)?,
        Some(TokenUrl::new(GOOGLE_TOKEN_URL.to_string()).map_err(|_| ApiError::Internal)?),
    )
    .set_redirect_uri(
        RedirectUrl::new(state.settings.google_redirect_uri.clone())
            .map_err(|_| ApiError::Internal)?,
    ))
}

pub fn create_github_client(state: &AppState) -> Result<BasicClient, ApiError> {
    if state.settings.github_client_id.is_empty() {
        return Err(ApiError::BadRequest("GitHub OAuth not configured".to_string()));
    }

    Ok(BasicClient::new(
        ClientId::new(state.settings.github_client_id.clone()),
        Some(ClientSecret::new(state.settings.github_client_secret.clone())),
        AuthUrl::new(GITHUB_AUTH_URL.to_string()).map_err(|_| ApiError::Internal)?,
        Some(TokenUrl::new(GITHUB_TOKEN_URL.to_string()).map_err(|_| ApiError::Internal)?),
    )
    .set_auth_type(AuthType::RequestBody)
    .set_redirect_uri(
        RedirectUrl::new(state.settings.github_redirect_uri.clone())
            .map_err(|_| ApiError::Internal)?,
    ))
}

pub fn generate_google_auth_url(state: &AppState) -> Result<(String, String), ApiError> {
    let client = create_google_client(state)?;
    let (auth_url, csrf_token) = client
        .authorize_url(CsrfToken::new_random)
        .add_scope(Scope::new("email".to_string()))
        .add_scope(Scope::new("profile".to_string()))
        .url();
    
    Ok((auth_url.to_string(), csrf_token.secret().clone()))
}

pub fn generate_github_auth_url(state: &AppState) -> Result<(String, String), ApiError> {
    let client = create_github_client(state)?;
    let (auth_url, csrf_token) = client
        .authorize_url(CsrfToken::new_random)
        .add_scope(Scope::new("user:email".to_string()))
        .url();
    
    Ok((auth_url.to_string(), csrf_token.secret().clone()))
}

pub async fn exchange_google_code(code: String, state: &AppState) -> Result<GoogleUserInfo, ApiError> {
    let client = create_google_client(state)?;
    let token = client
        .exchange_code(AuthorizationCode::new(code))
        .request_async(async_http_client)
        .await
        .map_err(|e| {
            tracing::error!("Failed to exchange Google code: {}", e);
            ApiError::BadRequest("Failed to exchange authorization code".to_string())
        })?;

    let user_info = state
        .http
        .get(GOOGLE_USERINFO_URL)
        .bearer_auth(token.access_token().secret())
        .send()
        .await
        .map_err(|e| {
            tracing::error!("Failed to fetch Google user info: {}", e);
            ApiError::Internal
        })?
        .json::<GoogleUserInfo>()
        .await
        .map_err(|e| {
            tracing::error!("Failed to parse Google user info: {}", e);
            ApiError::Internal
        })?;

    Ok(user_info)
}

pub async fn exchange_github_code(code: String, state: &AppState) -> Result<GitHubUserInfo, ApiError> {
    let client = create_github_client(state)?;
    let token = client
        .exchange_code(AuthorizationCode::new(code))
        .request_async(async_http_client)
        .await
        .map_err(|e| {
            tracing::error!("Failed to exchange GitHub code: {}", e);
            ApiError::BadRequest("Failed to exchange authorization code".to_string())
        })?;

    let access_token = token.access_token().secret();

    let mut user_info = state
        .http
        .get(GITHUB_USER_URL)
        .bearer_auth(access_token)
        .header("User-Agent", "CareerCompassAI")
        .send()
        .await
        .map_err(|e| {
            tracing::error!("Failed to fetch GitHub user info: {}", e);
            ApiError::Internal
        })?
        .json::<GitHubUserInfo>()
        .await
        .map_err(|e| {
            tracing::error!("Failed to parse GitHub user info: {}", e);
            ApiError::Internal
        })?;

    // If email is not public, fetch from emails endpoint
    if user_info.email.is_none() {
        let emails = state
            .http
            .get(GITHUB_EMAIL_URL)
            .bearer_auth(access_token)
            .header("User-Agent", "CareerCompassAI")
            .send()
            .await
            .map_err(|e| {
                tracing::error!("Failed to fetch GitHub emails: {}", e);
                ApiError::Internal
            })?
            .json::<Vec<GitHubEmail>>()
            .await
            .map_err(|e| {
                tracing::error!("Failed to parse GitHub emails: {}", e);
                ApiError::Internal
            })?;

        // Find primary verified email
        if let Some(primary_email) = emails.iter().find(|e| e.primary && e.verified) {
            user_info.email = Some(primary_email.email.clone());
        } else if let Some(first_verified) = emails.iter().find(|e| e.verified) {
            user_info.email = Some(first_verified.email.clone());
        }
    }

    Ok(user_info)
}
