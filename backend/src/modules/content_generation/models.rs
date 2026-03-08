use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone)]
pub struct ExtractedMetadata {
    pub candidate_name: String,
    pub recipient: String,
    pub company_name: String,
    pub position: String,
    pub years_experience: String,
    pub key_skills: String,
    pub certificates: Option<String>,
    pub email: Option<String>,
    pub phone: Option<String>,
    pub address: Option<String>,
}

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
    pub extracted_metadata: ExtractedMetadata,
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
    pub extracted_metadata: ExtractedMetadata,
}
