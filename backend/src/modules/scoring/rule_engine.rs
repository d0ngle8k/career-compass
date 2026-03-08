use std::collections::HashSet;

#[derive(Debug, Clone)]
pub struct RuleSignals {
    pub must_have_match: f64,
    pub semantic_overlap: f64,
    pub experience_fit: f64,
    pub section_completeness: f64,
    pub matched_skills: Vec<String>,
    pub missing_skills: Vec<String>,
    pub cv_years: Option<u8>,
    pub jd_years: Option<u8>,
}

pub fn evaluate_rules(
    cv_tokens: &HashSet<String>,
    jd_tokens: &HashSet<String>,
    cv_skills: &HashSet<String>,
    jd_skills: &HashSet<String>,
    cv_years: Option<u8>,
    jd_years: Option<u8>,
    section_completeness: f64,
) -> RuleSignals {
    let matched_skills = sorted_vec(intersection(cv_skills, jd_skills));
    let missing_skills = sorted_vec(difference(jd_skills, cv_skills));

    let must_have_match = if jd_skills.is_empty() {
        0.7
    } else {
        ratio(matched_skills.len(), jd_skills.len())
    };

    let semantic_overlap = jaccard(cv_tokens, jd_tokens);

    let experience_fit = match (cv_years, jd_years) {
        (Some(cv), Some(jd)) if jd > 0 => (cv as f64 / jd as f64).min(1.0),
        (Some(_), None) => 0.7,
        (None, Some(_)) => 0.3,
        (None, None) => 0.6,
        _ => 0.6,
    };

    RuleSignals {
        must_have_match,
        semantic_overlap,
        experience_fit,
        section_completeness,
        matched_skills,
        missing_skills,
        cv_years,
        jd_years,
    }
}

fn ratio(num: usize, den: usize) -> f64 {
    if den == 0 {
        return 0.0;
    }
    num as f64 / den as f64
}

fn jaccard(a: &HashSet<String>, b: &HashSet<String>) -> f64 {
    if a.is_empty() || b.is_empty() {
        return 0.0;
    }
    let inter = a.intersection(b).count() as f64;
    let union = a.union(b).count() as f64;
    if union == 0.0 {
        0.0
    } else {
        inter / union
    }
}

fn intersection(a: &HashSet<String>, b: &HashSet<String>) -> HashSet<String> {
    a.intersection(b).cloned().collect()
}

fn difference(a: &HashSet<String>, b: &HashSet<String>) -> HashSet<String> {
    a.difference(b).cloned().collect()
}

fn sorted_vec(input: HashSet<String>) -> Vec<String> {
    let mut out: Vec<String> = input.into_iter().collect();
    out.sort();
    out
}

#[cfg(test)]
mod tests {
    use super::evaluate_rules;
    use std::collections::HashSet;

    fn set(values: &[&str]) -> HashSet<String> {
        values.iter().map(|v| (*v).to_string()).collect()
    }

    #[test]
    fn computes_skill_matching_and_missing() {
        let cv_skills = set(&["rust", "react", "docker"]);
        let jd_skills = set(&["rust", "docker", "kubernetes"]);
        let cv_tokens = set(&["rust", "react", "backend"]);
        let jd_tokens = set(&["rust", "kubernetes", "backend"]);

        let s = evaluate_rules(&cv_tokens, &jd_tokens, &cv_skills, &jd_skills, Some(4), Some(5), 0.8);

        assert_eq!(s.matched_skills, vec!["docker", "rust"]);
        assert_eq!(s.missing_skills, vec!["kubernetes"]);
        assert!(s.must_have_match > 0.6);
        assert!(s.semantic_overlap > 0.3);
    }
}
