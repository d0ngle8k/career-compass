use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    #[error("unauthorized")]
    Unauthorized,
    #[error("bad request: {0}")]
    BadRequest(String),
    #[error("upstream error: {0}")]
    Upstream(String),
    #[error("internal error")]
    Internal,
}

#[derive(Serialize)]
struct ErrorBody {
    success: bool,
    error: String,
}

impl IntoResponse for ApiError {
    fn into_response(self) -> axum::response::Response {
        let status = match self {
            ApiError::Unauthorized => StatusCode::UNAUTHORIZED,
            ApiError::BadRequest(_) => StatusCode::BAD_REQUEST,
            ApiError::Upstream(_) => StatusCode::BAD_GATEWAY,
            ApiError::Internal => StatusCode::INTERNAL_SERVER_ERROR,
        };

        let body = Json(ErrorBody {
            success: false,
            error: self.to_string(),
        });

        (status, body).into_response()
    }
}
