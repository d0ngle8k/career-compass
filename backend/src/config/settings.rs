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
    
    // Database
    pub database_url: String,
    
    // Google OAuth
    pub google_client_id: String,
    pub google_client_secret: String,
    pub google_redirect_uri: String,
    
    // GitHub OAuth
    pub github_client_id: String,
    pub github_client_secret: String,
    pub github_redirect_uri: String,
    
    // Frontend URL for OAuth redirects
    pub frontend_url: String,
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
            admin_email: env::var("ADMIN_EMAIL").unwrap_or_else(|_| "admin@careercompass.local".to_string()),
            admin_password: env::var("ADMIN_PASSWORD").unwrap_or_else(|_| "".to_string()),
            gemini_api_key: env::var("GOOGLE_GEMINI_API_KEY")
                .map_err(|_| SettingsError::Missing("GOOGLE_GEMINI_API_KEY"))?,
            gemini_model: env::var("GOOGLE_GEMINI_MODEL").unwrap_or_else(|_| "gemini-1.5-flash".to_string()),
            nlp_service_url: env::var("NLP_SERVICE_URL")
                .unwrap_or_else(|_| "http://127.0.0.1:8001".to_string()),
            nlp_timeout_ms: env::var("NLP_TIMEOUT_MS")
                .unwrap_or_else(|_| "10000".to_string())
                .parse()?,
            
            // Database
            database_url: env::var("DATABASE_URL")
                .map_err(|_| SettingsError::Missing("DATABASE_URL"))?,
            
            // Google OAuth
            google_client_id: env::var("GOOGLE_CLIENT_ID")
                .unwrap_or_else(|_| "".to_string()),
            google_client_secret: env::var("GOOGLE_CLIENT_SECRET")
                .unwrap_or_else(|_| "".to_string()),
            google_redirect_uri: env::var("GOOGLE_REDIRECT_URI")
                .unwrap_or_else(|_| "http://localhost:9000/api/v1/auth/google/callback".to_string()),
            
            // GitHub OAuth
            github_client_id: env::var("GITHUB_CLIENT_ID")
                .unwrap_or_else(|_| "".to_string()),
            github_client_secret: env::var("GITHUB_CLIENT_SECRET")
                .unwrap_or_else(|_| "".to_string()),
            github_redirect_uri: env::var("GITHUB_REDIRECT_URI")
                .unwrap_or_else(|_| "http://localhost:9000/api/v1/auth/github/callback".to_string()),
            
            // Frontend URL
            frontend_url: env::var("FRONTEND_URL")
                .unwrap_or_else(|_| "http://localhost:8080".to_string()),
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
