use crate::{
    modules::content_generation::{
        models::{GenerateCoverLetterResponse, GenerateEmailResponse},
        template_engine,
    },
    shared::{api_error::ApiError, app_state::AppState},
};

pub async fn generate_email(
    _state: &AppState,
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<GenerateEmailResponse, ApiError> {
    let email_subject = template_engine::render_email_subject(cv_text, jd_text, language, style)
        .map_err(|e| ApiError::Upstream(format!("Template rendering failed: {e}")))?;
    
    let email_body = template_engine::render_email_body(cv_text, jd_text, language, style)
        .map_err(|e| ApiError::Upstream(format!("Template rendering failed: {e}")))?;
    
    Ok(GenerateEmailResponse {
        email_subject,
        email_body,
    })
}

pub async fn generate_cover_letter(
    _state: &AppState,
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<GenerateCoverLetterResponse, ApiError> {
    let cover_letter = template_engine::render_cover_letter(cv_text, jd_text, language, style)
        .map_err(|e| ApiError::Upstream(format!("Template rendering failed: {e}")))?;
    
    Ok(GenerateCoverLetterResponse { cover_letter })
}
