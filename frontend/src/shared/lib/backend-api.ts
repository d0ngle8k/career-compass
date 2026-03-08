const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:9000";

type LoginResponse = {
  success: boolean;
  data: {
    access_token: string;
    token_type: string;
    expires_in_minutes: number;
  };
};

type ApiEnvelope<T> = {
  success: boolean;
  data: T;
};

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export type ExtractedMetadata = {
  candidate_name: string;
  recipient: string;
  company_name: string;
  position: string;
  years_experience: string;
  key_skills: string;
  email?: string;
  phone?: string;
  address?: string;
};

const request = async <T>(path: string, init: RequestInit = {}, token?: string): Promise<T> => {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(init.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
  });

  const json = await response.json();

  if (!response.ok) {
    // If 401 Unauthorized, clear token from localStorage and redirect to login
    if (response.status === 401) {
      localStorage.removeItem("career-compass-token");
      localStorage.removeItem("career-compass-email");
      // Dispatch custom event so AuthContext can listen and update
      window.dispatchEvent(new Event("auth:unauthorized"));
    }
    throw new Error(json.error || "Request failed");
  }

  return json as T;
};

export const backendApi = {
  async register(email: string, password: string): Promise<ApiEnvelope<{ message: string; email: string }>> {
    return request<ApiEnvelope<{ message: string; email: string }>>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },

  async login(email: string, password: string): Promise<LoginResponse> {
    return request<LoginResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },

  async logout(token: string): Promise<void> {
    await request("/api/v1/auth/logout", { method: "POST" }, token);
  },

  async scoreCv(token: string, payload: { cv_text: string; jd_text: string; language: string }) {
    return request<ApiEnvelope<{ score: number; strengths: string[]; weaknesses: string[]; improvement_tips: string[] }>>(
      "/api/v1/ai/score-cv",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      token,
    );
  },

  async generateEmail(token: string, payload: { cv_text: string; jd_text: string; language: string; template_style?: string }) {
    return request<ApiEnvelope<{ email_subject: string; email_body: string; extracted_metadata: ExtractedMetadata }>>(
      "/api/v1/ai/generate-email",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      token,
    );
  },

  async generateCoverLetter(token: string, payload: { cv_text: string; jd_text: string; language: string; template_style?: string }) {
    return request<ApiEnvelope<{ cover_letter: string; extracted_metadata: ExtractedMetadata }>>(
      "/api/v1/ai/generate-cover-letter",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      token,
    );
  },

  async chatAssistant(
    token: string,
    payload: {
      message: string;
      language?: string;
      jd_text?: string;
      cv_summary?: string;
      history?: ChatMessage[];
    },
  ) {
    return request<ApiEnvelope<{ reply: string }>>(
      "/api/v1/ai/chat-assistant",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      token,
    );
  },
};
