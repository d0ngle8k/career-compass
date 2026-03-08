use axum::{routing::get, Router};

use crate::shared::app_state::AppState;

pub fn routes() -> Router<AppState> {
    Router::new().route("/health", get(handlers::health_check))
}

mod handlers;
