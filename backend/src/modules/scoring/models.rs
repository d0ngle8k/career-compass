use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct ScoreCvRequest {
    pub cv_text: String,
    pub jd_text: String,
    pub language: Option<String>,
}

#[derive(Serialize, Deserialize)]
pub struct ScoreCvResponse {
    pub score: f64,
    pub strengths: Vec<String>,
    pub weaknesses: Vec<String>,
    pub improvement_tips: Vec<String>,
}

#[derive(Deserialize)]
pub struct LegacyAnalyzeCvRequest {
    #[serde(alias = "cvText")]
    pub cv_text: String,
    #[serde(alias = "jdText")]
    pub jd_text: String,
    pub language: Option<String>,
    #[serde(alias = "templateStyle")]
    pub template_style: Option<String>,
    pub mode: Option<String>,
}

#[derive(Serialize, Deserialize)]
pub struct LegacyAnalyzeCvResponse {
    pub score: Option<f64>,
    pub strengths: Option<Vec<String>>,
    pub weaknesses: Option<Vec<String>>,
    pub improvement_tips: Option<Vec<String>>,
    pub email_subject: Option<String>,
    pub email_body: Option<String>,
    pub cover_letter: Option<String>,
}
