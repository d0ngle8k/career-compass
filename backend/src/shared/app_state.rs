use crate::config::settings::Settings;
use std::{collections::HashMap, sync::Arc, time::{Duration, Instant}};
use sqlx::PgPool;
use tokio::sync::RwLock;

#[derive(Clone)]
pub struct OAuthStateData {
    pub created: Instant,
    pub frontend_url: String,
}

#[derive(Clone)]
pub struct AppState {
    pub settings: Settings,
    pub http: reqwest::Client,
    pub db: PgPool,
    pub oauth_states: Arc<RwLock<HashMap<String, OAuthStateData>>>,
}

impl AppState {
    pub fn new(settings: Settings, db: PgPool) -> Self {
        Self {
            settings,
            http: reqwest::Client::new(),
            db,
            oauth_states: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    pub async fn store_oauth_state(&self, state: String, frontend_url: String) {
        let mut states = self.oauth_states.write().await;
        // Keep memory bounded by removing expired entries before adding a new one.
        let now = Instant::now();
        states.retain(|_, data| now.duration_since(data.created) <= Duration::from_secs(600));
        states.insert(
            state,
            OAuthStateData {
                created: now,
                frontend_url,
            },
        );
    }

    pub async fn consume_oauth_state(&self, state: &str) -> Option<String> {
        let mut states = self.oauth_states.write().await;
        if let Some(data) = states.remove(state) {
            if Instant::now().duration_since(data.created) <= Duration::from_secs(600) {
                return Some(data.frontend_url);
            }
        }
        None
    }
}
