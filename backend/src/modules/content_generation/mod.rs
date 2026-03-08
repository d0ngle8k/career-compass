use axum::{routing::post, Router};

use crate::shared::app_state::AppState;

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/generate-email", post(handlers::generate_email))
        .route("/generate-cover-letter", post(handlers::generate_cover_letter))
}

pub use handlers::{generate_cover_letter, generate_email};

mod handlers;
pub mod models;
pub mod service;
pub mod template_engine;
