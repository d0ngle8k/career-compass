use axum::{routing::post, Router};

use crate::shared::app_state::AppState;

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/score-cv", post(handlers::score_cv))
        .route("/analyze-cv", post(handlers::analyze_cv_legacy))
}

pub use handlers::{analyze_cv_legacy, score_cv};
pub mod models;
mod baseline;
mod handlers;
mod nlp_client;
mod regex_extractor;
mod rule_engine;
pub mod service;
