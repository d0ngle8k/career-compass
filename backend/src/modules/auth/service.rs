use crate::{shared::{api_error::ApiError, app_state::AppState}, modules::auth::jwt};

pub fn validate_credentials(email: &str, password: &str, state: &AppState) -> Result<(), ApiError> {
    let users = state.users.read().map_err(|_| ApiError::Internal)?;
    let stored_password = users.get(email).ok_or(ApiError::Unauthorized)?;

    if stored_password == password {
        return Ok(());
    }

    Err(ApiError::Unauthorized)
}

pub fn register(email: &str, password: &str, state: &AppState) -> Result<(), ApiError> {
    let normalized_email = email.trim().to_lowercase();
    if normalized_email.len() < 5 || !normalized_email.contains('@') {
        return Err(ApiError::BadRequest("Invalid email format".to_string()));
    }

    if password.len() < 6 {
        return Err(ApiError::BadRequest("Password must be at least 6 characters".to_string()));
    }

    let mut users = state.users.write().map_err(|_| ApiError::Internal)?;
    if users.contains_key(&normalized_email) {
        return Err(ApiError::BadRequest("Email already exists".to_string()));
    }

    users.insert(normalized_email, password.to_string());
    Ok(())
}

pub fn login(email: &str, state: &AppState) -> Result<String, ApiError> {
    jwt::generate_access_token(email, state)
}

pub fn validate_bearer_token(raw_token: &str, state: &AppState) -> Result<(), ApiError> {
    jwt::validate_token(raw_token, state).map(|_| ())
}
