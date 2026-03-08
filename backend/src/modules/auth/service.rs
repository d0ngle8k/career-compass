use crate::{
    shared::{api_error::ApiError, app_state::AppState},
    modules::auth::{jwt, models::{User, AuthProvider}},
};
use argon2::{
    Argon2,
    password_hash::{PasswordHash, PasswordHasher, PasswordVerifier, SaltString, rand_core::OsRng},
};

fn hash_password(password: &str) -> Result<String, ApiError> {
    let salt = SaltString::generate(&mut OsRng);
    let argon2 = Argon2::default();
    argon2
        .hash_password(password.as_bytes(), &salt)
        .map(|hash| hash.to_string())
        .map_err(|_| ApiError::Internal)
}

fn verify_password(stored_password: &str, provided_password: &str) -> Result<bool, ApiError> {
    if stored_password.starts_with("$argon2") {
        let parsed_hash = PasswordHash::new(stored_password).map_err(|_| ApiError::Internal)?;
        return Ok(Argon2::default()
            .verify_password(provided_password.as_bytes(), &parsed_hash)
            .is_ok());
    }

    // Backward-compatible fallback for legacy plain-text rows.
    Ok(stored_password == provided_password)
}

pub async fn validate_credentials(email: &str, password: &str, state: &AppState) -> Result<(), ApiError> {
    let user = sqlx::query_as!(
        User,
        r#"
        SELECT id, email, name, avatar_url, 
               provider as "provider: AuthProvider", 
               provider_id, password_hash, created_at, updated_at
        FROM users 
        WHERE email = $1 AND provider = 'email'
        "#,
        email
    )
    .fetch_optional(&state.db)
    .await
    .map_err(|_| ApiError::Internal)?
    .ok_or(ApiError::Unauthorized)?;

    let stored_password = user.password_hash.ok_or(ApiError::Unauthorized)?;

    if verify_password(&stored_password, password)? {
        // One-time migration path: upgrade legacy plain-text password to Argon2.
        if !stored_password.starts_with("$argon2") {
            let upgraded_hash = hash_password(password)?;
            if let Err(err) = sqlx::query!(
                "UPDATE users SET password_hash = $1, updated_at = NOW() WHERE id = $2",
                upgraded_hash,
                user.id
            )
            .execute(&state.db)
            .await
            {
                tracing::warn!("Failed to upgrade legacy password hash for {}: {}", email, err);
            }
        }
        return Ok(());
    }

    Err(ApiError::Unauthorized)
}

pub async fn register(email: &str, password: &str, state: &AppState) -> Result<(), ApiError> {
    let normalized_email = email.trim().to_lowercase();
    if normalized_email.len() < 5 || !normalized_email.contains('@') {
        return Err(ApiError::BadRequest("Invalid email format".to_string()));
    }

    if password.len() < 6 {
        return Err(ApiError::BadRequest("Password must be at least 6 characters".to_string()));
    }

    // Check if user already exists
    let existing = sqlx::query!(
        "SELECT id FROM users WHERE email = $1",
        normalized_email
    )
    .fetch_optional(&state.db)
    .await
    .map_err(|_| ApiError::Internal)?;

    if existing.is_some() {
        return Err(ApiError::BadRequest("Email already exists".to_string()));
    }

    let password_hash = hash_password(password)?;

    // Insert new user
    sqlx::query!(
        r#"
        INSERT INTO users (email, password_hash, provider)
        VALUES ($1, $2, 'email')
        "#,
        normalized_email,
        password_hash
    )
    .execute(&state.db)
    .await
    .map_err(|_| ApiError::Internal)?;

    Ok(())
}

pub fn login(email: &str, state: &AppState) -> Result<String, ApiError> {
    jwt::generate_access_token(email, state)
}

pub fn validate_bearer_token(raw_token: &str, state: &AppState) -> Result<(), ApiError> {
    jwt::validate_token(raw_token, state).map(|_| ())
}

pub async fn find_or_create_oauth_user(
    email: &str,
    name: Option<&str>,
    avatar_url: Option<&str>,
    provider_id: &str,
    provider: AuthProvider,
    state: &AppState,
) -> Result<User, ApiError> {
    if let Some(user) = sqlx::query_as!(
        User,
        r#"
        SELECT id, email, name, avatar_url, 
               provider as "provider: AuthProvider", 
               provider_id, password_hash, created_at, updated_at
        FROM users 
        WHERE provider = $1 AND provider_id = $2
        "#,
        provider as AuthProvider,
        provider_id
    )
    .fetch_optional(&state.db)
    .await
    .map_err(|_| ApiError::Internal)?
    {
        return Ok(user);
    }

    // Try to find by email (for account linking)
    if let Some(user) = sqlx::query_as!(
        User,
        r#"
        SELECT id, email, name, avatar_url, 
               provider as "provider: AuthProvider", 
               provider_id, password_hash, created_at, updated_at
        FROM users 
        WHERE email = $1
        "#,
        email
    )
    .fetch_optional(&state.db)
    .await
    .map_err(|_| ApiError::Internal)?
    {
        // Email exists but different provider → return existing user
        // In a more sophisticated system, we might want to link the accounts
        return Ok(user);
    }

    // Create new user
    let user = sqlx::query_as!(
        User,
        r#"
        INSERT INTO users (email, name, avatar_url, provider, provider_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, email, name, avatar_url, 
                  provider as "provider: AuthProvider", 
                  provider_id, password_hash, created_at, updated_at
        "#,
        email,
        name,
        avatar_url,
        provider as AuthProvider,
        provider_id
    )
    .fetch_one(&state.db)
    .await
    .map_err(|e| {
        tracing::error!("Failed to create OAuth user: {}", e);
        ApiError::Internal
    })?;

    Ok(user)
}
