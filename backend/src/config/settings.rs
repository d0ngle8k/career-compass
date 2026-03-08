use std::{env, num::ParseIntError};

#[derive(Clone, Debug)]
pub struct Settings {
    pub backend_host: String,
    pub backend_port: u16,
    pub jwt_secret: String,
    pub jwt_expires_minutes: i64,
    pub admin_email: String,
    pub admin_password: String,
    pub gemini_api_key: String,
    pub gemini_model: String,
    pub nlp_service_url: String,
    pub nlp_timeout_ms: u64,
}

impl Settings {
    pub fn from_env() -> Result<Self, SettingsError> {
        Ok(Self {
            backend_host: env::var("BACKEND_HOST").unwrap_or_else(|_| "127.0.0.1".to_string()),
            backend_port: env::var("BACKEND_PORT")
                .unwrap_or_else(|_| "9000".to_string())
                .parse()?,
            jwt_secret: env::var("JWT_SECRET").map_err(|_| SettingsError::Missing("JWT_SECRET"))?,
            jwt_expires_minutes: env::var("JWT_EXPIRES_MINUTES")
                .unwrap_or_else(|_| "120".to_string())
                .parse()?,
            admin_email: env::var("ADMIN_EMAIL").map_err(|_| SettingsError::Missing("ADMIN_EMAIL"))?,
            admin_password: env::var("ADMIN_PASSWORD").map_err(|_| SettingsError::Missing("ADMIN_PASSWORD"))?,
            gemini_api_key: env::var("GOOGLE_GEMINI_API_KEY")
                .map_err(|_| SettingsError::Missing("GOOGLE_GEMINI_API_KEY"))?,
            gemini_model: env::var("GOOGLE_GEMINI_MODEL").unwrap_or_else(|_| "gemini-1.5-flash".to_string()),
            nlp_service_url: env::var("NLP_SERVICE_URL")
                .unwrap_or_else(|_| "http://127.0.0.1:8001".to_string()),
            nlp_timeout_ms: env::var("NLP_TIMEOUT_MS")
                .unwrap_or_else(|_| "1200".to_string())
                .parse()?,
        })
    }
}

#[derive(thiserror::Error, Debug)]
pub enum SettingsError {
    #[error("missing required environment variable: {0}")]
    Missing(&'static str),
    #[error("invalid numeric value in environment: {0}")]
    ParseInt(#[from] ParseIntError),
}
