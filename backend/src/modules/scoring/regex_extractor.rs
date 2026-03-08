use regex::Regex;
use std::collections::HashSet;

pub fn extract_max_years(text: &str) -> Option<u8> {
    let re = Regex::new(r"(?i)\b(\d{1,2})\s*\+?\s*(years?|yrs?|n[aă]m)\b")
        .expect("valid year regex");

    re.captures_iter(text)
        .filter_map(|cap| cap.get(1).and_then(|m| m.as_str().parse::<u8>().ok()))
        .max()
}

pub fn extract_required_years_from_jd(jd_text: &str) -> Option<u8> {
    extract_max_years(jd_text)
}

pub fn extract_present_skills(text: &str) -> HashSet<String> {
    let lower = text.to_lowercase();
    let mut found = HashSet::new();

    for skill in supported_skills() {
        if contains_skill(&lower, skill) {
            found.insert(skill.to_string());
        }
    }

    found
}

fn contains_skill(text: &str, skill: &str) -> bool {
    // Use escaped regex to avoid false positives for special characters (e.g., c++, c#).
    let pattern = format!(r"(?i)(^|[^a-z0-9]){}([^a-z0-9]|$)", regex::escape(skill));
    Regex::new(&pattern)
        .map(|re| re.is_match(text))
        .unwrap_or(false)
}

fn supported_skills() -> &'static [&'static str] {
    &[
        "rust",
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "docker",
        "kubernetes",
        "aws",
        "gcp",
        "azure",
        "git",
        "linux",
        "redis",
        "graphql",
        "grpc",
        "tailwind",
    ]
}

#[cfg(test)]
mod tests {
    use super::{extract_max_years, extract_present_skills, extract_required_years_from_jd};

    #[test]
    fn extracts_years_in_english_and_vietnamese() {
        let text = "I have 3 years of backend exp and 5 năm in software overall";
        assert_eq!(extract_max_years(text), Some(5));
    }

    #[test]
    fn extracts_required_years_from_jd() {
        let jd = "Require at least 4 years experience in backend development";
        assert_eq!(extract_required_years_from_jd(jd), Some(4));
    }

    #[test]
    fn extracts_skills_from_text() {
        let text = "Worked with Rust, React, PostgreSQL and Docker";
        let skills = extract_present_skills(text);
        assert!(skills.contains("rust"));
        assert!(skills.contains("react"));
        assert!(skills.contains("postgresql"));
        assert!(skills.contains("docker"));
    }
}
