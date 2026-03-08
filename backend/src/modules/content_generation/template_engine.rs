use regex::Regex;
use std::sync::OnceLock;
use tera::{Context, Tera};

static TEMPLATES: OnceLock<Tera> = OnceLock::new();

pub fn init_templates() -> Result<(), tera::Error> {
    let tera = Tera::new("templates/**/*.tera")?;
    TEMPLATES.set(tera).map_err(|_| {
        tera::Error::msg("Failed to initialize templates - already initialized")
    })?;
    Ok(())
}

fn get_templates() -> &'static Tera {
    TEMPLATES.get().expect("Templates not initialized")
}

/// Extract candidate name from CV text
fn extract_candidate_name(cv_text: &str) -> String {
    // Look for patterns like "Name: John Doe" or first line if it looks like a name
    let lines: Vec<&str> = cv_text.lines().collect();
    
    // Check for "Name:" pattern
    let name_re = Regex::new(r"(?i)name\s*[:：]\s*(.+)").unwrap();
    for line in &lines {
        if let Some(captures) = name_re.captures(line) {
            if let Some(name) = captures.get(1) {
                return name.as_str().trim().to_string();
            }
        }
    }
    
    // Check for "Họ và tên:" pattern (Vietnamese)
    let name_vi_re = Regex::new(r"(?i)(họ và tên|tên|full name)\s*[:：]\s*(.+)").unwrap();
    for line in &lines {
        if let Some(captures) = name_vi_re.captures(line) {
            if let Some(name) = captures.get(2) {
                return name.as_str().trim().to_string();
            }
        }
    }
    
    // Fallback: use first non-empty line (assumed to be name in many CVs)
    for line in lines {
        let trimmed = line.trim();
        if !trimmed.is_empty() && trimmed.len() < 50 {
            return trimmed.to_string();
        }
    }
    
    "Ứng viên".to_string() // Default fallback
}

/// Extract years of experience from CV
fn extract_years_experience(cv_text: &str) -> String {
    let years_re = Regex::new(r"(\d+)\s*\+?\s*(year|năm|years)").unwrap();
    
    if let Some(captures) = years_re.captures(cv_text) {
        if let Some(years) = captures.get(1) {
            return years.as_str().to_string();
        }
    }
    
    "3".to_string() // Default fallback
}

/// Extract email from CV
fn extract_email(cv_text: &str) -> Option<String> {
    let email_re = Regex::new(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b").unwrap();
    
    email_re
        .find(cv_text)
        .map(|m| m.as_str().to_string())
}

/// Extract phone from CV
fn extract_phone(cv_text: &str) -> Option<String> {
    let phone_re = Regex::new(r"(\+?\d{1,4}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?[\d\s.-]{7,}").unwrap();
    
    phone_re
        .find(cv_text)
        .map(|m| m.as_str().to_string())
}

/// Extract key skills from CV (simplified - could be enhanced with NLP)
fn extract_key_skills(cv_text: &str) -> String {
    let lower = cv_text.to_lowercase();
    let mut skills = Vec::new();
    
    // Common tech skills
    let skill_patterns = [
        "python", "java", "javascript", "typescript", "react", "vue", "angular",
        "node", "docker", "kubernetes", "aws", "gcp", "azure", "sql", "mongodb",
        "postgresql", "redis", "kafka", "rust", "go", "c++", "c#", ".net",
        "spring boot", "django", "flask", "fastapi", "tensorflow", "pytorch",
        "machine learning", "deep learning", "ai", "data science"
    ];
    
    for skill in skill_patterns {
        if lower.contains(skill) {
            skills.push(skill);
        }
    }
    
    if skills.is_empty() {
        return "software development, problem solving, teamwork".to_string();
    }
    
    skills.into_iter().take(5).collect::<Vec<_>>().join(", ")
}

/// Extract company name from JD
fn extract_company_name(jd_text: &str) -> String {
    // Look for "Company:" or "Công ty:" patterns
    let company_re = Regex::new(r"(?i)(company|công ty)\s*[:：]\s*(.+)").unwrap();
    
    for line in jd_text.lines() {
        if let Some(captures) = company_re.captures(line) {
            if let Some(name) = captures.get(2) {
                return name.as_str().trim().to_string();
            }
        }
    }
    
    "công ty".to_string() // Default fallback
}

/// Extract position title from JD
fn extract_position(jd_text: &str) -> String {
    let lines: Vec<&str> = jd_text.lines().collect();
    
    // Look for "Position:" or "Vị trí:" patterns
    let position_re = Regex::new(r"(?i)(position|vị trí|job title|chức danh)\s*[:：]\s*(.+)").unwrap();
    
    for line in &lines {
        if let Some(captures) = position_re.captures(line) {
            if let Some(pos) = captures.get(2) {
                return pos.as_str().trim().to_string();
            }
        }
    }
    
    // Fallback: use first line
    for line in lines {
        let trimmed = line.trim();
        if !trimmed.is_empty() && trimmed.len() < 100 {
            return trimmed.to_string();
        }
    }
    
    "Software Developer".to_string()
}

/// Build template context from CV and JD
fn build_context(cv_text: &str, jd_text: &str) -> Context {
    let mut context = Context::new();
    
    context.insert("candidate_name", &extract_candidate_name(cv_text));
    context.insert("years_experience", &extract_years_experience(cv_text));
    context.insert("key_skills", &extract_key_skills(cv_text));
    context.insert("company_name", &extract_company_name(jd_text));
    context.insert("position", &extract_position(jd_text));
    context.insert("recipient", "Hiring Manager");
    
    if let Some(email) = extract_email(cv_text) {
        context.insert("email", &email);
    }
    
    if let Some(phone) = extract_phone(cv_text) {
        context.insert("phone", &phone);
    }
    
    context
}

/// Render email subject template
pub fn render_email_subject(
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<String, tera::Error> {
    let template_name = format!("email_subject_{}_{}.tera", style, language);
    let context = build_context(cv_text, jd_text);
    
    get_templates().render(&template_name, &context)
}

/// Render email body template
pub fn render_email_body(
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<String, tera::Error> {
    let template_name = format!("email_body_{}_{}.tera", style, language);
    let context = build_context(cv_text, jd_text);
    
    get_templates().render(&template_name, &context)
}

/// Render cover letter template
pub fn render_cover_letter(
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<String, tera::Error> {
    let template_name = format!("cover_letter_{}_{}.tera", style, language);
    let context = build_context(cv_text, jd_text);
    
    get_templates().render(&template_name, &context)
}
