use crate::config::settings::Settings;
use sqlx::PgPool;

#[derive(Clone)]
pub struct AppState {
    pub settings: Settings,
    pub http: reqwest::Client,
    pub db: PgPool,
}

impl AppState {
    pub fn new(settings: Settings, db: PgPool) -> Self {
        Self {
            settings,
            http: reqwest::Client::new(),
            db,
        }
    }
}
