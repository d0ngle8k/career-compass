mod config;
mod modules;
mod shared;

use axum::Router;
use axum::http::{HeaderValue, Method};
use config::settings::Settings;
use modules::{ai, auth, content_generation, health, scoring};
use shared::{app_state::AppState, database};
use std::net::SocketAddr;
use tower_http::cors::{Any, CorsLayer};
use tracing::{error, info};

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    let settings = Settings::from_env().expect("failed to load settings");
    let host = settings.backend_host.clone();
    let port = settings.backend_port;
    
    // Initialize database connection pool
    info!("Connecting to database...");
    let db_pool = match database::create_pool(&settings.database_url).await {
        Ok(pool) => {
            info!("Database connection pool created successfully");
            pool
        }
        Err(err) => {
            error!("Failed to create database pool: {}", err);
            error!("Please ensure PostgreSQL is running and DATABASE_URL is correct");
            std::process::exit(1);
        }
    };
    
    // Run database migrations
    info!("Running database migrations...");
    if let Err(err) = database::run_migrations(&db_pool).await {
        error!("Failed to run database migrations: {}", err);
        std::process::exit(1);
    }
    
    // Initialize templates
    if let Err(e) = content_generation::template_engine::init_templates() {
        error!("Failed to initialize templates: {}", e);
        std::process::exit(1);
    }
    info!("Templates initialized successfully");
    
    let state = AppState::new(settings, db_pool);
    
    // Build CORS allowed origins
    let mut allowed_origins = vec![
        HeaderValue::from_static("http://localhost:8080"),
        HeaderValue::from_static("http://127.0.0.1:8080"),
        HeaderValue::from_static("http://localhost:5173"),
        HeaderValue::from_static("http://127.0.0.1:5173"),
        HeaderValue::from_static("http://localhost:5174"),
        HeaderValue::from_static("http://127.0.0.1:5174"),
    ];
    
    // Add production frontend URL from environment
    let frontend_url = &state.settings.frontend_url;
    if !frontend_url.starts_with("http://localhost") && !frontend_url.starts_with("http://127.0.0.1") {
        if let Ok(origin) = HeaderValue::from_str(frontend_url) {
            info!("Adding production frontend origin: {}", frontend_url);
            allowed_origins.push(origin);
        }
    }
    
    let cors = CorsLayer::new()
        .allow_origin(allowed_origins)
        .allow_methods([Method::GET, Method::POST, Method::OPTIONS])
        .allow_headers(Any);

    let app = Router::new()
        .nest("/api/v1/auth", auth::routes())
        .nest("/api/v1/ai", ai::routes())
        .nest("/api/v1/scoring", scoring::routes())
        .nest("/api/v1/content", content_generation::routes())
        .merge(health::routes())
        .layer(cors)
        .with_state(state);

    let addr: SocketAddr = format!("{host}:{port}")
        .parse()
        .expect("invalid BACKEND_HOST/BACKEND_PORT");

    let listener = match tokio::net::TcpListener::bind(addr).await {
        Ok(listener) => listener,
        Err(err) => {
            error!(
                "failed to bind {}: {}. Another backend process may already be running on this port.",
                addr, err
            );
            error!(
                "Stop the existing process or change BACKEND_PORT in backend/.env, then retry."
            );
            return;
        }
    };

    info!("backend listening on http://{}", addr);

    if let Err(err) = axum::serve(listener, app).await {
        error!("failed to start backend server: {}", err);
    }
}
