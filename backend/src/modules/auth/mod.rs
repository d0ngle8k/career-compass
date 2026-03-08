use axum::{routing::post, Router};

use crate::shared::app_state::AppState;

pub fn routes() -> Router<AppState> {
    Router::new()
    .route("/register", post(handlers::register))
        .route("/login", post(handlers::login))
        .route("/logout", post(handlers::logout))
}

mod handlers;
mod jwt;
mod models;
pub mod service;
