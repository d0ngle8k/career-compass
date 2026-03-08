pub fn chat_assistant_prompt(
    message: &str,
    language: &str,
    jd_text: Option<&str>,
    cv_summary: Option<&str>,
    history_lines: &[String],
) -> String {
    let mut prompt = format!(
        "You are CVGenius AI Assistant. Your role is to help users improve CV quality, interview readiness, and job application content.\n\nRules:\n- Keep advice practical and specific.\n- If the user asks outside CV/career context, gently steer back to career support.\n- Use concise sections and examples when useful.\n- Answer in language: {language}.\n"
    );

    if let Some(cv) = cv_summary.filter(|v| !v.trim().is_empty()) {
        prompt.push_str(&format!("\nCV context (may be partial):\n{cv}\n"));
    }

    if let Some(jd) = jd_text.filter(|v| !v.trim().is_empty()) {
        prompt.push_str(&format!("\nTarget job description:\n{jd}\n"));
    }

    if !history_lines.is_empty() {
        prompt.push_str("\nRecent conversation:\n");
        prompt.push_str(&history_lines.join("\n"));
        prompt.push('\n');
    }

    prompt.push_str(&format!("\nUser question: {message}\n\nRespond as plain text, no JSON."));
    prompt
}
