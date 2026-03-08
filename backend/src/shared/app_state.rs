use crate::config::settings::Settings;
use std::{collections::HashMap, sync::{Arc, RwLock}};

#[derive(Clone)]
pub struct AppState {
    pub settings: Settings,
    pub http: reqwest::Client,
    pub users: Arc<RwLock<HashMap<String, String>>>,
}

impl AppState {
    pub fn new(settings: Settings) -> Self {
        let mut users = HashMap::new();
        users.insert(settings.admin_email.clone(), settings.admin_password.clone());

        Self {
            settings,
            http: reqwest::Client::new(),
            users: Arc::new(RwLock::new(users)),
        }
    }
}
