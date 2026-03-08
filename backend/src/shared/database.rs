use sqlx::{postgres::PgPoolOptions, PgPool};
use std::time::Duration;

pub async fn create_pool(database_url: &str) -> Result<PgPool, sqlx::Error> {
    PgPoolOptions::new()
        .max_connections(5)
        .acquire_timeout(Duration::from_secs(3))
        .connect(database_url)
        .await
}

pub async fn run_migrations(pool: &PgPool) -> Result<(), sqlx::Error> {
    // Note: In production, use sqlx-cli for migrations
    // For now, we'll run the SQL directly
    let migration_sql = include_str!("../../migrations/001_create_users_table.sql");
    
    // Execute migration
    sqlx::raw_sql(migration_sql)
        .execute(pool)
        .await?;
    
    tracing::info!("Database migrations completed successfully");
    Ok(())
}
