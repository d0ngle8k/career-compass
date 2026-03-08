use chrono::{Duration, Utc};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};

use crate::{
    modules::auth::models::Claims,
    shared::{api_error::ApiError, app_state::AppState},
};

pub fn generate_access_token(email: &str, state: &AppState) -> Result<String, ApiError> {
    let exp = Utc::now() + Duration::minutes(state.settings.jwt_expires_minutes);
    let claims = Claims {
        sub: email.to_string(),
        exp: exp.timestamp() as usize,
    };

    encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(state.settings.jwt_secret.as_bytes()),
    )
    .map_err(|_| ApiError::Internal)
}

pub fn validate_token(token: &str, state: &AppState) -> Result<Claims, ApiError> {
    decode::<Claims>(
        token,
        &DecodingKey::from_secret(state.settings.jwt_secret.as_bytes()),
        &Validation::default(),
    )
    .map(|token_data| token_data.claims)
    .map_err(|_| ApiError::Unauthorized)
}
