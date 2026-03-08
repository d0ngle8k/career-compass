use axum::{routing::post, Router};

use crate::modules::{content_generation, scoring};
use crate::shared::app_state::AppState;

pub fn routes() -> Router<AppState> {
    Router::new()
        .route("/chat-assistant", post(handlers::chat_assistant))
        // Backward compatibility routes: keep old /api/v1/ai/* surface for frontend.
        .route("/analyze-cv", post(scoring::analyze_cv_legacy))
        .route("/score-cv", post(scoring::score_cv))
        .route("/generate-email", post(content_generation::generate_email))
        .route(
            "/generate-cover-letter",
            post(content_generation::generate_cover_letter),
        )
}

pub mod gemini_client;
mod handlers;
mod models;
mod prompt_templates;
mod service;
