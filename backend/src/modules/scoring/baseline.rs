use crate::modules::scoring::{
    models::ScoreCvResponse,
    regex_extractor::{extract_max_years, extract_present_skills, extract_required_years_from_jd},
    rule_engine::{evaluate_rules, RuleSignals},
};
use std::collections::HashSet;

pub fn score_cv_baseline(cv_text: &str, jd_text: &str, language: &str) -> ScoreCvResponse {
    let cv_tokens = tokenize(cv_text);
    let jd_tokens = tokenize(jd_text);

    let cv_skills = extract_present_skills(cv_text);
    let jd_skills = extract_present_skills(jd_text);

    let cv_years = extract_max_years(cv_text);
    let jd_years = extract_required_years_from_jd(jd_text);
    let section_score = section_completeness(cv_text, language);

    let signals = evaluate_rules(
        &cv_tokens,
        &jd_tokens,
        &cv_skills,
        &jd_skills,
        cv_years,
        jd_years,
        section_score,
    );

    let mut score = 100.0
        * (0.50 * signals.must_have_match
            + 0.20 * signals.semantic_overlap
            + 0.20 * signals.experience_fit
            + 0.10 * signals.section_completeness);

    let missing_must_have = signals.missing_skills.len();
    if missing_must_have >= 3 {
        score -= 12.0;
    } else if missing_must_have >= 1 {
        score -= 5.0;
    }

    let score = score.clamp(0.0, 100.0);

    let (strengths, weaknesses, tips) = explain(signals);

    ScoreCvResponse {
        score: (score * 10.0).round() / 10.0,
        strengths,
        weaknesses,
        improvement_tips: tips,
    }
}

fn tokenize(text: &str) -> HashSet<String> {
    text.to_lowercase()
        .split(|c: char| !c.is_alphanumeric() && c != '+' && c != '#')
        .map(str::trim)
        .filter(|token| token.len() >= 2)
        .map(str::to_string)
        .collect()
}

fn section_completeness(cv_text: &str, language: &str) -> f64 {
    let lower = cv_text.to_lowercase();
    let required_sections = if language.eq_ignore_ascii_case("vi") {
        vec!["kinh nghiệm", "kỹ năng", "học vấn", "dự án"]
    } else {
        vec!["experience", "skills", "education", "project"]
    };

    let found = required_sections
        .iter()
        .filter(|section| lower.contains(*section))
        .count();

    found as f64 / required_sections.len() as f64
}

fn explain(signals: RuleSignals) -> (Vec<String>, Vec<String>, Vec<String>) {
    let mut strengths = Vec::new();
    let mut weaknesses = Vec::new();
    let mut tips = Vec::new();

    let total_required = signals.matched_skills.len() + signals.missing_skills.len();

    if !signals.matched_skills.is_empty() {
        let match_rate = if total_required > 0 {
            (signals.matched_skills.len() as f64 / total_required as f64) * 100.0
        } else {
            0.0
        };
        strengths.push(format!(
            "Technical match: {}/{} skills ({:.1}%). Strong matches: {}",
            signals.matched_skills.len(),
            total_required,
            match_rate,
            signals
                .matched_skills
                .iter()
                .take(5)
                .cloned()
                .collect::<Vec<_>>()
                .join(", ")
        ));
    }

    if signals.semantic_overlap >= 0.35 {
        strengths.push("Content alignment is good: CV language is close to JD priorities.".to_string());
    }

    if let (Some(cv), Some(jd)) = (signals.cv_years, signals.jd_years) {
        if cv >= jd {
            strengths.push(format!(
                "Experience meets requirement ({} years vs {} years required).",
                cv, jd
            ));
        } else {
            weaknesses.push(format!(
                "Experience gap: {} years in CV vs {} years required.",
                cv, jd
            ));
            tips.push(
                "Offset the experience gap by highlighting project scope, ownership, and measurable impact."
                    .to_string(),
            );
        }
    }

    if !signals.missing_skills.is_empty() {
        weaknesses.push(format!(
            "Missing or unclear required skills ({}): {}",
            signals.missing_skills.len(),
            signals
                .missing_skills
                .iter()
                .take(6)
                .cloned()
                .collect::<Vec<_>>()
                .join(", ")
        ));
        tips.push(
            "For each missing skill, add one bullet with action + tool + measurable result (%, revenue, users, time saved)."
                .to_string(),
        );
    }

    if signals.section_completeness < 0.75 {
        weaknesses.push(
            "CV structure is incomplete (missing standard sections like experience/skills/education/projects)."
                .to_string(),
        );
        tips.push(
            "Add missing sections and keep headings ATS-friendly: Summary, Skills, Experience, Projects, Education."
                .to_string(),
        );
    }

    if strengths.is_empty() {
        strengths.push("CV has some relevant signals but key strengths are not clearly mapped to JD requirements.".to_string());
    }

    if weaknesses.is_empty() {
        weaknesses.push("No critical gaps detected in baseline checks; remaining improvements are mostly optimization.".to_string());
    }

    if tips.is_empty() {
        tips.push(
            "Tailor the CV summary and top bullets to exact JD keywords and quantified outcomes."
                .to_string(),
        );
    }

    (strengths, weaknesses, tips)
}

#[cfg(test)]
mod tests {
    use super::score_cv_baseline;

    #[test]
    fn strong_match_gets_higher_score() {
        let cv = "Experience\nSoftware engineer with 5 years in Rust and Docker.\nSkills\nRust Docker PostgreSQL\nEducation\nBS Computer Science\nProjects\nBuilt scalable backend systems.";
        let jd = "Looking for backend engineer with 4 years of experience in Rust, Docker, PostgreSQL.";

        let result = score_cv_baseline(cv, jd, "en");
        assert!(result.score >= 70.0, "score was {}", result.score);
        assert!(!result.strengths.is_empty());
    }

    #[test]
    fn weak_match_gets_lower_score_and_tips() {
        let cv = "Experience\n1 year internship\nSkills\nExcel PowerPoint\nEducation\nBusiness";
        let jd = "Need software engineer with 4 years in Rust, Docker, Kubernetes and PostgreSQL.";

        let result = score_cv_baseline(cv, jd, "en");
        assert!(result.score <= 60.0, "score was {}", result.score);
        assert!(!result.improvement_tips.is_empty());
    }
}
