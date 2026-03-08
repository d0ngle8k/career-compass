use crate::{
    modules::ai::{
        gemini_client,
        models::{ChatAssistantResponse, ChatMessage},
        prompt_templates,
    },
    shared::{api_error::ApiError, app_state::AppState},
};

pub async fn chat_assistant(
    state: &AppState,
    message: &str,
    language: &str,
    jd_text: Option<&str>,
    cv_summary: Option<&str>,
    history: Option<&[ChatMessage]>,
) -> Result<ChatAssistantResponse, ApiError> {
    let history_lines = history
        .unwrap_or(&[])
        .iter()
        .rev()
        .take(8)
        .collect::<Vec<_>>()
        .into_iter()
        .rev()
        .map(|item| format!("{}: {}", item.role, item.content))
        .collect::<Vec<_>>();

    let prompt = prompt_templates::chat_assistant_prompt(
        message,
        language,
        jd_text,
        cv_summary,
        &history_lines,
    );
    let reply = gemini_client::generate_text(state, prompt).await?;

    Ok(ChatAssistantResponse {
        reply: reply.trim().to_string(),
    })
}
