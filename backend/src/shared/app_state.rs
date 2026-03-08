use crate::config::settings::Settings;
use std::{collections::HashMap, sync::Arc, time::{Duration, Instant}};
use sqlx::PgPool;
use tokio::sync::RwLock;

#[derive(Clone)]
pub struct AppState {
    pub settings: Settings,
    pub http: reqwest::Client,
    pub db: PgPool,
    pub oauth_states: Arc<RwLock<HashMap<String, Instant>>>,
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

    pub async fn store_oauth_state(&self, state: String) {
        let mut states = self.oauth_states.write().await;
        // Keep memory bounded by removing expired entries before adding a new one.
        let now = Instant::now();
        states.retain(|_, created| now.duration_since(*created) <= Duration::from_secs(600));
        states.insert(state, now);
    }

    pub async fn consume_oauth_state(&self, state: &str) -> bool {
        let mut states = self.oauth_states.write().await;
        if let Some(created) = states.remove(state) {
            return Instant::now().duration_since(created) <= Duration::from_secs(600);
        }
        false
    }
}
