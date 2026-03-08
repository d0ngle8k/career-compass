use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct GenerateEmailRequest {
    pub cv_text: String,
    pub jd_text: String,
    pub language: Option<String>,
    pub template_style: Option<String>,
}

#[derive(Serialize, Deserialize)]
pub struct GenerateEmailResponse {
    pub email_subject: String,
    pub email_body: String,
}

#[derive(Deserialize)]
pub struct GenerateCoverLetterRequest {
    pub cv_text: String,
    pub jd_text: String,
    pub language: Option<String>,
    pub template_style: Option<String>,
}

#[derive(Serialize, Deserialize)]
pub struct GenerateCoverLetterResponse {
    pub cover_letter: String,
}
