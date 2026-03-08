use regex::Regex;
use std::sync::OnceLock;
use tera::{Context, Tera};

use crate::modules::content_generation::models::ExtractedMetadata;

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

fn normalize_style(style: &str) -> &'static str {
    match style.trim().to_lowercase().as_str() {
        "formal" => "formal",
        "casual" => "casual",
        "concise" => "concise",
        "persuasive" => "persuasive",
        // Backward compatibility for old frontend values.
        "modern" => "casual",
        "creative" => "persuasive",
        _ => "auto",
    }
}

fn auto_style_from_jd(jd_text: &str, language: &str) -> &'static str {
    let jd_lower = jd_text.to_lowercase();
    let lang = language.trim().to_lowercase();

    let formal_markers_vi = ["tập đoàn", "ngân hàng", "tuân thủ", "quy trình", "enterprise"];
    let formal_markers_en = ["corporation", "bank", "compliance", "governance", "enterprise"];
    let persuasive_markers = ["marketing", "sales", "growth", "brand", "business development"];
    let concise_markers = ["startup", "fast-paced", "remote", "product", "agile"];

    if persuasive_markers.iter().any(|m| jd_lower.contains(m)) {
        return "persuasive";
    }
    if concise_markers.iter().any(|m| jd_lower.contains(m)) {
        return "concise";
    }

    if lang == "vi" {
        if formal_markers_vi.iter().any(|m| jd_lower.contains(m)) {
            return "formal";
        }
        return "casual";
    }

    if formal_markers_en.iter().any(|m| jd_lower.contains(m)) {
        return "formal";
    }

    "casual"
}

fn resolve_style(style: &str, jd_text: &str, language: &str) -> &'static str {
    let normalized = normalize_style(style);
    if normalized == "auto" {
        return auto_style_from_jd(jd_text, language);
    }
    normalized
}

fn clean_line(line: &str) -> String {
    line.replace('\u{feff}', "")
        .replace('\t', " ")
    .replace('|', " ")
    .replace('•', " ")
    .replace('●', " ")
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ")
}

fn trim_trailing_punctuation(text: &str) -> String {
    text.trim()
        .trim_end_matches(|c: char| [',', ';', ':', '.'].contains(&c))
        .trim()
        .to_string()
}

fn looks_like_name(line: &str) -> bool {
    let trimmed = line.trim();
    if trimmed.is_empty() || trimmed.len() < 4 || trimmed.len() > 60 {
        return false;
    }

    let lower = trimmed.to_lowercase();
    let blocked_tokens = [
        "curriculum vitae",
        "resume",
        "cv",
        "email",
        "phone",
        "địa chỉ",
        "address",
        "kinh nghiệm",
        "experience",
        "kỹ năng",
        "skills",
        "objective",
        "summary",
        "điện thoại",
        "sđt",
        "liên hệ",
        "contact",
        "github",
        "linkedin",
        "mục tiêu",
    ];
    if blocked_tokens.iter().any(|token| lower.contains(token)) {
        return false;
    }

    let digit_count = trimmed.chars().filter(|c| c.is_ascii_digit()).count();
    if digit_count > 0 {
        return false;
    }

    let words = trimmed.split_whitespace().collect::<Vec<_>>();
    if !(2..=6).contains(&words.len()) {
        return false;
    }

    let has_letters = Regex::new(r"(?u)\p{L}+").unwrap().is_match(trimmed);
    has_letters
}

/// Extract candidate name from CV text
fn extract_candidate_name(cv_text: &str) -> String {
    let lines: Vec<String> = cv_text.lines().map(clean_line).collect();

    let labeled_name_re = Regex::new(
        r"(?i)(họ\s*và\s*tên|full\s*name|name|candidate\s*name|ứng\s*viên)\s*[:：-]\s*([^,\n;]{1,100})",
    )
    .unwrap();
    for line in &lines {
        if let Some(captures) = labeled_name_re.captures(line) {
            if let Some(name) = captures.get(2) {
                let value = clean_line(name.as_str());
                if looks_like_name(&value) {
                    return value;
                }
            }
        }
    }

    for line in &lines {
        if looks_like_name(line) {
            return line.clone();
        }
    }

    // Vietnamese full-name pattern fallback (supports diacritics).
    let vn_name_re = Regex::new(r"(?u)\b([\p{Lu}\p{L}]{2,}(?:\s+[\p{Lu}\p{L}]{2,}){1,5})\b").unwrap();
    for line in &lines {
        if let Some(captures) = vn_name_re.captures(line) {
            if let Some(value) = captures.get(1) {
                let candidate = clean_line(value.as_str());
                if looks_like_name(&candidate) {
                    return candidate;
                }
            }
        }
    }

    "Ứng viên".to_string()
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
    let email_re = Regex::new(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b").unwrap();
    
    email_re
        .find(cv_text)
        .map(|m| m.as_str().to_string())
}

/// Extract phone from CV
fn extract_phone(cv_text: &str) -> Option<String> {
    // First try labeled format
    let labeled_phone_re = Regex::new(r"(?i)(phone|điện\s*thoại|sdt|s\.?đ\.?t|mobile)\s*[:：-]\s*([\d+\-\s\.\(\)]{8,20})").unwrap();
    
    if let Some(captures) = labeled_phone_re.captures(cv_text) {
        if let Some(phone_str) = captures.get(2) {
            let phone = phone_str.as_str().trim();
            let digit_count = phone.chars().filter(|c| c.is_ascii_digit()).count();
            if (9..=15).contains(&digit_count) {
                return Some(phone.to_string());
            }
        }
    }
    
    // Fallback: generic phone pattern
    let phone_re = Regex::new(r"\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d[\d\s.-]{6,16}\d").unwrap();

    for m in phone_re.find_iter(cv_text) {
        let candidate = m.as_str().trim();
        let digit_count = candidate.chars().filter(|c| c.is_ascii_digit()).count();
        if (9..=15).contains(&digit_count) {
            return Some(candidate.to_string());
        }
    }

    None
}

/// Extract address from CV
fn extract_address(cv_text: &str) -> Option<String> {
    let labeled_address_re = Regex::new(r"(?i)(địa\s*chỉ|address)\s*[:：-]\s*(.+)").unwrap();
    for line in cv_text.lines() {
        if let Some(captures) = labeled_address_re.captures(line) {
            if let Some(value) = captures.get(2) {
                let address = clean_line(value.as_str());
                if address.len() >= 8 {
                    return Some(address);
                }
            }
        }
    }

    let address_hint_re = Regex::new(
        r"(?i)\b(đường|duong|street|st\.|phường|phuong|ward|quận|quan|district|thành\s*phố|tp\.?|city|hồ\s*chí\s*minh|ha\s*noi|hà\s*nội|xã|xa|huyện|huyen|tỉnh|tinh|ấp|ap|khu\s*phố|so\s*nha|số\s*nhà)\b",
    )
    .unwrap();
    for line in cv_text.lines() {
        let normalized = clean_line(line);
        let comma_count = normalized.matches(',').count();
        if normalized.len() >= 10
            && normalized.len() <= 140
            && (address_hint_re.is_match(&normalized) || comma_count >= 2)
        {
            return Some(normalized);
        }
    }

    None
}

/// Extract key skills from CV (simplified - could be enhanced with NLP)
fn extract_key_skills(cv_text: &str) -> String {
    let lower = cv_text.to_lowercase();
    
    // Try to find and extract from SKILLS section first
    // Look for section headers like "SKILLS:", "TECHNICAL SKILLS", etc.
    let section_match = cv_text
        .lines()
        .enumerate()
        .find(|(_, line)| {
            let lower_line = line.to_lowercase();
            lower_line.contains("technical skills")
                || (lower_line.contains("skills") && !lower_line.contains("soft skills"))
                || lower_line.contains("competencies")
                || lower_line.contains("core skills")
        });
    
    if let Some((start_idx, _)) = section_match {
        let mut skills = Vec::new();
        
        // Collect lines after the section header until we hit another section
        for (idx, line) in cv_text.lines().enumerate().skip(start_idx + 1) {
            let trimmed = line.trim();
            if trimmed.is_empty() {
                continue;
            }
            
            // Check if this looks like a section header (all caps, no commas, no bullets)
            // Section headers are typically all caps with minimal punctuation
            let looks_like_section_header = trimmed.to_uppercase() == trimmed
                && !trimmed.contains(',')
                && !trimmed.starts_with("•")
                && !trimmed.starts_with("-")
                && !trimmed.starts_with("*")
                && trimmed.split_whitespace().count() <= 3
                && (trimmed.contains("EXPERIENCE")
                    || trimmed.contains("EDUCATION")
                    || trimmed.contains("CERTIF")
                    || trimmed.contains("PROJECT")
                    || trimmed.contains("AWARD")
                    || trimmed.contains("LANGUAGE"));

            if looks_like_section_header {
                break;
            }
            
            let cleaned_line = clean_line(line);
            let parts: Vec<String> = cleaned_line
                .split(|c: char| c == ',' || c == ' ')
                .filter(|s| {
                    let s_lower = s.to_lowercase();
                    // Filter out common words and symbols
                    !["and", "or", "the", "a", "an", "-", "•", "*", "+"].contains(&s_lower.as_str())
                        && s.len() > 1
                })
                .map(|s| s.to_string())
                .collect();
            
            skills.extend(parts);
        }
        
        if !skills.is_empty() {
            // Remove duplicates while preserving order
            let mut unique_skills = Vec::new();
            let mut seen = std::collections::HashSet::new();
            for skill in skills {
                let skill_lower = skill.to_lowercase();
                if !seen.contains(&skill_lower) && skill.len() > 1 {
                    unique_skills.push(skill);
                    seen.insert(skill_lower);
                }
            }
            
            if !unique_skills.is_empty() {
                return unique_skills.join(", ");
            }
        }
    }
    
    // Fallback: Pattern matching with common tech skills
    let mut skills = Vec::new();
    let skill_patterns = [
        "python", "java", "javascript", "typescript", "react", "vue", "angular",
        "node", "docker", "kubernetes", "aws", "gcp", "azure", "sql", "mongodb",
        "postgresql", "redis", "kafka", "rust", "go", "c++", "c#", ".net",
        "spring boot", "django", "flask", "fastapi", "tensorflow", "pytorch",
        "machine learning", "deep learning", "ai", "data science", "git", "linux",
        "jenkins", "terraform", "ci/cd", "agile"
    ];
    
    for skill in skill_patterns {
        if lower.contains(skill) {
            skills.push(skill);
        }
    }
    
    if skills.is_empty() {
        return "software development, problem solving, teamwork".to_string();
    }
    
    skills.into_iter().collect::<Vec<_>>().join(", ")
}

/// Extract certificates from CV
fn extract_certificates(cv_text: &str) -> Option<String> {
    // Look for CERTIFICATES, CERTIFICATIONS, or CREDENTIALS section
    let section_match = cv_text
        .lines()
        .enumerate()
        .find(|(_, line)| {
            let lower_line = line.to_lowercase();
            lower_line.contains("certificates")
                || lower_line.contains("certifications")
                || lower_line.contains("credentials")
        });
    
    if let Some((start_idx, _)) = section_match {
        let mut certificates = Vec::new();
        
        // Collect lines after the section header until we hit another section
        for (idx, line) in cv_text.lines().enumerate().skip(start_idx + 1) {
            let trimmed = line.trim();
            if trimmed.is_empty() {
                continue;
            }
            
            // Check if this looks like a section header (all caps, keywords)
            let looks_like_section_header = trimmed.to_uppercase() == trimmed
                && !trimmed.contains(',')
                && !trimmed.starts_with("•")
                && !trimmed.starts_with("-")
                && !trimmed.starts_with("*")
                && trimmed.split_whitespace().count() <= 3
                && (trimmed.contains("EXPERIENCE")
                    || trimmed.contains("EDUCATION")
                    || trimmed.contains("SKILLS")
                    || trimmed.contains("PROJECT")
                    || trimmed.contains("AWARD")
                    || trimmed.contains("LANGUAGE")
                    || trimmed.contains("WORK")
                    || trimmed.contains("PROFESSIONAL"));

            if looks_like_section_header {
                break;
            }
            
            if !trimmed.is_empty() {
                let cleaned = clean_line(trimmed);
                
                // Remove bullet points, dashes, and numbers at the start
                let cert = cleaned
                    .trim_start_matches(|c: char| {
                        c == '•' || c == '*' || c == '-' || c == '+' || c.is_numeric()
                    })
                    .trim_start_matches(|c: char| c == '.' || c == ')' || c == ':')
                    .trim();
                
                if cert.len() > 3 {
                    certificates.push(cert.to_string());
                }
            }
        }
        
        if !certificates.is_empty() {
            return Some(certificates.join("; "));
        }
    }
    
    None
}

/// Extract company name from JD
fn extract_company_name(jd_text: &str) -> String {
    let company_re = Regex::new(r"(?i)(company|công\s*ty|employer|organization)\s*[:：-]\s*([^,\n;]{1,100})").unwrap();

    // First try to find labeled company name
    for line in jd_text.lines() {
        if let Some(captures) = company_re.captures(line) {
            if let Some(name) = captures.get(2) {
                let extracted = trim_trailing_punctuation(&clean_line(name.as_str()));
                if !extracted.is_empty() && extracted.len() <= 100 {
                    return extracted;
                }
            }
        }
    }

    // Fallback to finding lines that look like company name candidates
    for line in jd_text.lines() {
        let normalized = clean_line(line);
        if (normalized.len() >= 3 && normalized.len() <= 80) && 
           !normalized.to_lowercase().contains("position") &&
           !normalized.to_lowercase().contains("role") &&
           !normalized.to_lowercase().contains("dear") &&
           !normalized.to_lowercase().contains("kính") {
            // If line contains title-like text indicating company
            if normalized.to_lowercase().contains("company") || 
               normalized.to_lowercase().contains("công ty") ||
               normalized.to_lowercase().contains("corporation") ||
               normalized.to_lowercase().contains("group") {
                return normalized;
            }
        }
    }

    "Company".to_string()
}

/// Extract recipient (contact person or department) from JD
fn extract_recipient(jd_text: &str, language: &str) -> String {
    let lang_is_vi = language.trim().to_lowercase().contains("vi");
    
    // Step 1: Try English-specific patterns first if not Vietnamese
    if !lang_is_vi {
        // Pattern 1: "Manager: [Name]" or "Hiring Manager: [Name]"
        let manager_re = Regex::new(r"(?i)(?:hiring\s*)?manager\s*[:：]\s*([A-Za-z\s\.\-]{2,80}?)(?:\n|$)").unwrap();
        for line in jd_text.lines() {
            let normalized = clean_line(line);
            if let Some(captures) = manager_re.captures(&normalized) {
                if let Some(value) = captures.get(1) {
                    let recipient = trim_trailing_punctuation(&clean_line(value.as_str()));
                    if !recipient.is_empty() && recipient.len() >= 2 && recipient.len() <= 80 {
                        return recipient;
                    }
                }
            }
        }
        
        // Pattern 2: "Contact[/Person]: [Name]"
        let contact_re = Regex::new(r"(?i)(?:contact|contact\s*person|hiring\s*lead)\s*[:：]\s*([A-Za-z\s\.\-]{2,80}?)(?:\n|$)").unwrap();
        for line in jd_text.lines() {
            let normalized = clean_line(line);
            if let Some(captures) = contact_re.captures(&normalized) {
                if let Some(value) = captures.get(1) {
                    let recipient = trim_trailing_punctuation(&clean_line(value.as_str()));
                    if !recipient.is_empty() && recipient.len() >= 2 && recipient.len() <= 80 {
                        return recipient;
                    }
                }
            }
        }
        
        // Pattern 3: "Dear [Name]" (in English JD)
        let dear_re = Regex::new(r"(?i)dear\s+([A-Za-z\s\.\-]{2,80}?)(?:[,.]|$)").unwrap();
        for line in jd_text.lines() {
            let normalized = clean_line(line);
            if let Some(captures) = dear_re.captures(&normalized) {
                if let Some(value) = captures.get(1) {
                    let recipient = trim_trailing_punctuation(&clean_line(value.as_str()));
                    if !recipient.is_empty() && recipient.len() >= 2 && recipient.len() <= 80 {
                        return recipient;
                    }
                }
            }
        }
    }
    
    // Step 2: Try Vietnamese-specific patterns
    if lang_is_vi || true {  // Always try Vietnamese patterns as fallback
        // Pattern 1: "Kính gửi: [Name]" or "Thư gửi: [Name]"
        let kính_re = Regex::new(r"(?i)(?:kính|thư)\s*gửi\s*[:：]\s*([^,\n;]{2,80}?)(?:\n|$)").unwrap();
        for line in jd_text.lines() {
            let normalized = clean_line(line);
            if let Some(captures) = kính_re.captures(&normalized) {
                if let Some(value) = captures.get(1) {
                    let recipient = trim_trailing_punctuation(&clean_line(value.as_str()));
                    if !recipient.is_empty() && recipient.len() >= 2 && recipient.len() <= 80 {
                        return recipient;
                    }
                }
            }
        }
        
        // Pattern 2: "Người liên hệ: [Name]" or "Liên hệ: [Name]"
        let contact_vi_re = Regex::new(r"(?i)(?:người\s*)?liên\s*hệ\s*[:：]\s*([^,\n;]{2,80}?)(?:\n|$)").unwrap();
        for line in jd_text.lines() {
            let normalized = clean_line(line);
            if let Some(captures) = contact_vi_re.captures(&normalized) {
                if let Some(value) = captures.get(1) {
                    let recipient = trim_trailing_punctuation(&clean_line(value.as_str()));
                    if !recipient.is_empty() && recipient.len() >= 2 && recipient.len() <= 80 {
                        return recipient;
                    }
                }
            }
        }
    }
    
    // Step 3: Fallback to generic pattern
    let generic_re = Regex::new(
        r"(?i)(?:kính|dear|contact|manager|người\s*liên\s*hệ)\s*[:：]?\s*([^\n;]{2,80})"
    ).unwrap();
    
    for line in jd_text.lines() {
        let normalized = clean_line(line);
        if let Some(captures) = generic_re.captures(&normalized) {
            if let Some(value) = captures.get(1) {
                let recipient = trim_trailing_punctuation(&clean_line(value.as_str()));
                if !recipient.is_empty() 
                    && recipient.len() >= 2 
                    && recipient.len() <= 80 
                    && !recipient.to_lowercase().contains("company")
                    && !recipient.to_lowercase().contains("position")
                    && !recipient.to_lowercase().contains("role") {
                    return recipient;
                }
            }
        }
    }

    // Step 4: Return appropriate language-specific default
    if lang_is_vi {
        "Anh/Chị phụ trách tuyển dụng".to_string()
    } else {
        "Hiring Manager".to_string()
    }
}

/// Extract position title from JD
fn extract_position(jd_text: &str) -> String {
    let lines: Vec<String> = jd_text.lines().map(clean_line).collect();

    let position_re =
        Regex::new(r"(?i)(position|vị\s*trí|job\s*title|chức\s*danh|role)\s*[:：-]\s*([^,\n;]{1,100})")
            .unwrap();

    // First try to find labeled position
    for line in &lines {
        if let Some(captures) = position_re.captures(line) {
            if let Some(pos) = captures.get(2) {
                let value = trim_trailing_punctuation(&clean_line(pos.as_str()));
                if !value.is_empty() && value.len() <= 100 {
                    return value;
                }
            }
        }
    }

    // Fallback: look for known job titles
    let role_hint_re = Regex::new(
        r"(?i)\b(software\s*engineer|backend\s*developer|frontend\s*developer|full\s*stack|data\s*analyst|data\s*scientist|devops|marketing\s*specialist|hr\s*specialist|product\s*manager|engineer|developer|designer|manager|specialist)\b",
    )
    .unwrap();
    
    for line in &lines {
        let normalized = clean_line(line);
        if (normalized.len() >= 3 && normalized.len() <= 80) && 
           role_hint_re.is_match(&normalized) &&
           !normalized.to_lowercase().contains("company") &&
           !normalized.to_lowercase().contains("dear") {
            return normalized.clone();
        }
    }

    "Software Engineer".to_string()
}

/// Build template context from CV and JD
fn build_context(cv_text: &str, jd_text: &str, language: &str) -> Context {
    let mut context = Context::new();

    let metadata = extract_metadata(cv_text, jd_text, language);

    context.insert("candidate_name", &metadata.candidate_name);
    context.insert("years_experience", &metadata.years_experience);
    context.insert("key_skills", &metadata.key_skills);
    context.insert("company_name", &metadata.company_name);
    context.insert("position", &metadata.position);
    context.insert("recipient", &metadata.recipient);

    if let Some(email) = &metadata.email {
        context.insert("email", email);
    }

    if let Some(phone) = &metadata.phone {
        context.insert("phone", phone);
    }

    if let Some(address) = &metadata.address {
        context.insert("address", address);
    }
    
    if let Some(certificates) = &metadata.certificates {
        context.insert("certificates", certificates);
    }
    
    context
}

pub fn extract_metadata(cv_text: &str, jd_text: &str, language: &str) -> ExtractedMetadata {
    ExtractedMetadata {
        candidate_name: extract_candidate_name(cv_text),
        recipient: extract_recipient(jd_text, language),
        company_name: extract_company_name(jd_text),
        position: extract_position(jd_text),
        years_experience: extract_years_experience(cv_text),
        key_skills: extract_key_skills(cv_text),
        certificates: extract_certificates(cv_text),
        email: extract_email(cv_text),
        phone: extract_phone(cv_text),
        address: extract_address(cv_text),
    }
}

/// Render email subject template
pub fn render_email_subject(
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<String, tera::Error> {
    let selected_style = resolve_style(style, jd_text, language);
    let template_name = format!("email_subject_{}_{}.tera", selected_style, language);
    let context = build_context(cv_text, jd_text, language);
    
    get_templates().render(&template_name, &context)
}

/// Render email body template
pub fn render_email_body(
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<String, tera::Error> {
    let selected_style = resolve_style(style, jd_text, language);
    let template_name = format!("email_body_{}_{}.tera", selected_style, language);
    let context = build_context(cv_text, jd_text, language);
    
    get_templates().render(&template_name, &context)
}

/// Render cover letter template
pub fn render_cover_letter(
    cv_text: &str,
    jd_text: &str,
    language: &str,
    style: &str,
) -> Result<String, tera::Error> {
    let selected_style = resolve_style(style, jd_text, language);
    let template_name = format!("cover_letter_{}_{}.tera", selected_style, language);
    let context = build_context(cv_text, jd_text, language);
    
    get_templates().render(&template_name, &context)
}
