use crate::{
    modules::{
        content_generation,
        scoring::{
            baseline,
            models::{LegacyAnalyzeCvResponse, ScoreCvResponse},
            nlp_client,
        },
    },
    shared::{api_error::ApiError, app_state::AppState},
};
use tracing::warn;

pub async fn score_cv(
    state: &AppState,
    cv_text: &str,
    jd_text: &str,
    language: &str,
) -> Result<ScoreCvResponse, ApiError> {
    match nlp_client::score_cv(state, cv_text, jd_text, language).await {
        Ok(result) => Ok(result),
        Err(err) => {
            warn!("NLP scoring failed, falling back to baseline: {}", err);
            Ok(baseline::score_cv_baseline(cv_text, jd_text, language))
        }
    }
}

pub async fn analyze_cv_legacy(
    state: &AppState,
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
    mode: &str,
) -> Result<LegacyAnalyzeCvResponse, ApiError> {
    let mut response = LegacyAnalyzeCvResponse {
        score: None,
        strengths: None,
        weaknesses: None,
        improvement_tips: None,
        email_subject: None,
        email_body: None,
        cover_letter: None,
    };

    match mode {
        "score_only" => {
            let score = score_cv(state, cv_text, jd_text, language).await?;
            response.score = Some(score.score);
            response.strengths = Some(score.strengths);
            response.weaknesses = Some(score.weaknesses);
            response.improvement_tips = Some(score.improvement_tips);
        }
        "email_only" => {
            let email =
                content_generation::service::generate_email(state, cv_text, jd_text, language, style)
                    .await?;
            response.email_subject = Some(email.email_subject);
            response.email_body = Some(email.email_body);
        }
        "cover_letter_only" => {
            let letter = content_generation::service::generate_cover_letter(
                state, cv_text, jd_text, language, style,
            )
            .await?;
            response.cover_letter = Some(letter.cover_letter);
        }
        _ => {
            let score = score_cv(state, cv_text, jd_text, language).await?;
            let email =
                content_generation::service::generate_email(state, cv_text, jd_text, language, style)
                    .await?;
            let letter = content_generation::service::generate_cover_letter(
                state, cv_text, jd_text, language, style,
            )
            .await?;

            response.score = Some(score.score);
            response.strengths = Some(score.strengths);
            response.weaknesses = Some(score.weaknesses);
            response.improvement_tips = Some(score.improvement_tips);
            response.email_subject = Some(email.email_subject);
            response.email_body = Some(email.email_body);
            response.cover_letter = Some(letter.cover_letter);
        }
    }

    Ok(response)
}
