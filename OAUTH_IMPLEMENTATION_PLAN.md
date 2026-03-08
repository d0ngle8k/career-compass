# Kế hoạch triển khai OAuth Google & GitHub

## 📋 Phân tích hệ thống hiện tại

### Backend (Rust + Axum)
- ✅ JWT authentication đã có
- ✅ In-memory user storage (HashMap)
- ✅ Endpoints: `/register`, `/login`, `/logout`
- ⚠️ Chưa có database persistence → cần migrate trước khi production

### Frontend (React + TypeScript)
- ✅ AuthContext với localStorage
- ✅ Login/Signup pages
- ✅ Protected routes

### Hạn chế hiện tại
- **Chỉ hỗ trợ email/password**
- **Không có database** → users mất khi restart server
- **Không có user profiles** → chỉ lưu email + password

---

## 🎯 Mục tiêu OAuth Implementation

### Tính năng chính
1. **OAuth Google Login** - đăng nhập qua tài khoản Google
2. **OAuth GitHub Login** - đăng nhập qua tài khoản GitHub
3. **Account linking** - liên kết nhiều providers cho cùng 1 user
4. **Seamless flow** - tự động tạo tài khoản nếu lần đầu đăng nhập

### User Experience Flow
```
┌─────────────┐
│ Login Page  │
└──────┬──────┘
       │
       ├─► Email/Password (existing)
       │
       ├─► [Sign in with Google]  ──► Google OAuth ──► Backend callback ──► JWT token
       │
       └─► [Sign in with GitHub]  ──► GitHub OAuth ──► Backend callback ──► JWT token
```

---

## 🏗️ Kiến trúc kỹ thuật

### 1. Backend Architecture (Rust + Axum)

#### A. Dependencies cần thêm vào `Cargo.toml`
```toml
[dependencies]
# ... existing dependencies

# OAuth 2.0 support
oauth2 = "4.4"
url = "2.5"
base64 = "0.22"

# Database (recommended để persist users)
sqlx = { version = "0.8", features = ["runtime-tokio-rustls", "postgres", "chrono", "uuid"] }
uuid = { version = "1.10", features = ["v4", "serde"] }
```

#### B. User Model mở rộng

**File: `backend/src/modules/auth/models.rs`**

```rust
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AuthProvider {
    Email,
    Google,
    GitHub,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: String,                          // UUID
    pub email: String,
    pub name: Option<String>,
    pub avatar_url: Option<String>,
    pub provider: AuthProvider,
    pub provider_id: Option<String>,         // Google/GitHub user ID
    pub password_hash: Option<String>,       // Chỉ có nếu provider = Email
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Deserialize)]
pub struct OAuthCallbackRequest {
    pub code: String,
    pub state: String,
}

#[derive(Serialize)]
pub struct OAuthInitResponse {
    pub authorization_url: String,
}
```

#### C. OAuth Configuration

**File: `backend/src/config/settings.rs`** - thêm vào struct Settings:

```rust
pub struct Settings {
    // ... existing fields
    
    // Google OAuth
    pub google_client_id: String,
    pub google_client_secret: String,
    pub google_redirect_uri: String,
    
    // GitHub OAuth
    pub github_client_id: String,
    pub github_client_secret: String,
    pub github_redirect_uri: String,
    
    // Frontend URL for redirects
    pub frontend_url: String,
}
```

**Cập nhật `.env` file:**
```env
# ... existing vars

# Google OAuth (lấy từ Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:9000/api/auth/google/callback

# GitHub OAuth (lấy từ GitHub Settings > Developer settings)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:9000/api/auth/github/callback

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

#### D. OAuth Service Implementation

**File mới: `backend/src/modules/auth/oauth.rs`**

```rust
use oauth2::{
    AuthUrl, AuthorizationCode, ClientId, ClientSecret, CsrfToken,
    RedirectUrl, Scope, TokenResponse, TokenUrl,
    basic::BasicClient,
    reqwest::async_http_client,
};
use serde::Deserialize;
use crate::shared::{api_error::ApiError, app_state::AppState};

// Google OAuth URLs
const GOOGLE_AUTH_URL: &str = "https://accounts.google.com/o/oauth2/v2/auth";
const GOOGLE_TOKEN_URL: &str = "https://oauth2.googleapis.com/token";
const GOOGLE_USERINFO_URL: &str = "https://www.googleapis.com/oauth2/v2/userinfo";

// GitHub OAuth URLs
const GITHUB_AUTH_URL: &str = "https://github.com/login/oauth/authorize";
const GITHUB_TOKEN_URL: &str = "https://github.com/login/oauth/access_token";
const GITHUB_USER_URL: &str = "https://api.github.com/user";

#[derive(Debug, Deserialize)]
pub struct GoogleUserInfo {
    pub id: String,
    pub email: String,
    pub name: Option<String>,
    pub picture: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct GitHubUserInfo {
    pub id: u64,
    pub email: Option<String>,
    pub login: String,
    pub name: Option<String>,
    pub avatar_url: Option<String>,
}

pub fn create_google_client(state: &AppState) -> Result<BasicClient, ApiError> {
    Ok(BasicClient::new(
        ClientId::new(state.settings.google_client_id.clone()),
        Some(ClientSecret::new(state.settings.google_client_secret.clone())),
        AuthUrl::new(GOOGLE_AUTH_URL.to_string()).map_err(|_| ApiError::Internal)?,
        Some(TokenUrl::new(GOOGLE_TOKEN_URL.to_string()).map_err(|_| ApiError::Internal)?),
    )
    .set_redirect_uri(
        RedirectUrl::new(state.settings.google_redirect_uri.clone())
            .map_err(|_| ApiError::Internal)?,
    ))
}

pub fn create_github_client(state: &AppState) -> Result<BasicClient, ApiError> {
    Ok(BasicClient::new(
        ClientId::new(state.settings.github_client_id.clone()),
        Some(ClientSecret::new(state.settings.github_client_secret.clone())),
        AuthUrl::new(GITHUB_AUTH_URL.to_string()).map_err(|_| ApiError::Internal)?,
        Some(TokenUrl::new(GITHUB_TOKEN_URL.to_string()).map_err(|_| ApiError::Internal)?),
    )
    .set_redirect_uri(
        RedirectUrl::new(state.settings.github_redirect_uri.clone())
            .map_err(|_| ApiError::Internal)?,
    ))
}

pub fn generate_google_auth_url(state: &AppState) -> Result<(String, String), ApiError> {
    let client = create_google_client(state)?;
    let (auth_url, csrf_token) = client
        .authorize_url(CsrfToken::new_random)
        .add_scope(Scope::new("email".to_string()))
        .add_scope(Scope::new("profile".to_string()))
        .url();
    
    Ok((auth_url.to_string(), csrf_token.secret().clone()))
}

pub fn generate_github_auth_url(state: &AppState) -> Result<(String, String), ApiError> {
    let client = create_github_client(state)?;
    let (auth_url, csrf_token) = client
        .authorize_url(CsrfToken::new_random)
        .add_scope(Scope::new("user:email".to_string()))
        .url();
    
    Ok((auth_url.to_string(), csrf_token.secret().clone()))
}

pub async fn exchange_google_code(code: String, state: &AppState) -> Result<GoogleUserInfo, ApiError> {
    let client = create_google_client(state)?;
    let token = client
        .exchange_code(AuthorizationCode::new(code))
        .request_async(async_http_client)
        .await
        .map_err(|_| ApiError::BadRequest("Failed to exchange code".to_string()))?;

    let user_info = state
        .http
        .get(GOOGLE_USERINFO_URL)
        .bearer_auth(token.access_token().secret())
        .send()
        .await
        .map_err(|_| ApiError::Internal)?
        .json::<GoogleUserInfo>()
        .await
        .map_err(|_| ApiError::Internal)?;

    Ok(user_info)
}

pub async fn exchange_github_code(code: String, state: &AppState) -> Result<GitHubUserInfo, ApiError> {
    let client = create_github_client(state)?;
    let token = client
        .exchange_code(AuthorizationCode::new(code))
        .request_async(async_http_client)
        .await
        .map_err(|_| ApiError::BadRequest("Failed to exchange code".to_string()))?;

    let user_info = state
        .http
        .get(GITHUB_USER_URL)
        .bearer_auth(token.access_token().secret())
        .header("User-Agent", "CareerCompassAI")
        .send()
        .await
        .map_err(|_| ApiError::Internal)?
        .json::<GitHubUserInfo>()
        .await
        .map_err(|_| ApiError::Internal)?;

    Ok(user_info)
}
```

#### E. OAuth Handlers

**File: `backend/src/modules/auth/handlers.rs`** - thêm handlers mới:

```rust
use axum::{extract::{Query, State}, response::Redirect};
use crate::modules::auth::{oauth, models::OAuthCallbackRequest};

/// Google OAuth: Bước 1 - Redirect user đến Google consent screen
pub async fn google_login(
    State(state): State<AppState>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let (auth_url, csrf_token) = oauth::generate_google_auth_url(&state)?;
    
    // TODO: Lưu csrf_token vào session/cache để verify callback
    // Tạm thời skip CSRF validation cho đơn giản
    
    Ok(ok(OAuthInitResponse { authorization_url: auth_url }))
}

/// Google OAuth: Bước 2 - Handle callback từ Google
pub async fn google_callback(
    State(state): State<AppState>,
    Query(params): Query<OAuthCallbackRequest>,
) -> Result<Redirect, ApiError> {
    // TODO: Verify CSRF token
    
    let user_info = oauth::exchange_google_code(params.code, &state).await?;
    
    // Tìm hoặc tạo user trong database
    let user = find_or_create_oauth_user(
        &user_info.email,
        user_info.name.as_deref(),
        user_info.picture.as_deref(),
        &user_info.id,
        AuthProvider::Google,
        &state,
    )?;
    
    // Tạo JWT token
    let token = service::login(&user.email, &state)?;
    
    // Redirect về frontend với token
    let redirect_url = format!(
        "{}/?token={}&email={}",
        state.settings.frontend_url,
        token,
        urlencoding::encode(&user.email)
    );
    
    Ok(Redirect::to(&redirect_url))
}

/// GitHub OAuth: Bước 1
pub async fn github_login(
    State(state): State<AppState>,
) -> Result<impl axum::response::IntoResponse, ApiError> {
    let (auth_url, _csrf_token) = oauth::generate_github_auth_url(&state)?;
    Ok(ok(OAuthInitResponse { authorization_url: auth_url }))
}

/// GitHub OAuth: Bước 2
pub async fn github_callback(
    State(state): State<AppState>,
    Query(params): Query<OAuthCallbackRequest>,
) -> Result<Redirect, ApiError> {
    let user_info = oauth::exchange_github_code(params.code, &state).await?;
    
    let email = user_info.email.unwrap_or_else(|| format!("{}@github.local", user_info.login));
    
    let user = find_or_create_oauth_user(
        &email,
        user_info.name.as_deref(),
        user_info.avatar_url.as_deref(),
        &user_info.id.to_string(),
        AuthProvider::GitHub,
        &state,
    )?;
    
    let token = service::login(&user.email, &state)?;
    
    let redirect_url = format!(
        "{}/?token={}&email={}",
        state.settings.frontend_url,
        token,
        urlencoding::encode(&user.email)
    );
    
    Ok(Redirect::to(&redirect_url))
}

// Helper function (cần implement trong service.rs)
fn find_or_create_oauth_user(
    email: &str,
    name: Option<&str>,
    avatar_url: Option<&str>,
    provider_id: &str,
    provider: AuthProvider,
    state: &AppState,
) -> Result<User, ApiError> {
    // TODO: Implement với database
    // Tạm thời dùng in-memory HashMap (không lý tưởng)
    unimplemented!("Cần implement user persistence với database")
}
```

#### F. Router Update

**File: `backend/src/modules/auth/mod.rs`** - thêm routes:

```rust
use axum::{
    routing::{get, post},
    Router,
};

pub fn routes() -> Router<AppState> {
    Router::new()
        // Existing routes
        .route("/register", post(handlers::register))
        .route("/login", post(handlers::login))
        .route("/logout", post(handlers::logout))
        
        // OAuth routes
        .route("/google/login", get(handlers::google_login))
        .route("/google/callback", get(handlers::google_callback))
        .route("/github/login", get(handlers::github_login))
        .route("/github/callback", get(handlers::github_callback))
}
```

---

### 2. Frontend Architecture (React + TypeScript)

#### A. OAuth UI Components

**File mới: `frontend/src/features/auth/components/OAuthButtons.tsx`**

```tsx
import { Button } from "@/components/ui/button";
import { Chrome, Github } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:9000";

export const OAuthButtons = () => {
  const [loading, setLoading] = useState<"google" | "github" | null>(null);

  const handleGoogleLogin = async () => {
    setLoading("google");
    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/google/login`);
      const data = await response.json();
      
      if (data.success && data.data.authorization_url) {
        // Redirect user đến Google OAuth consent screen
        window.location.href = data.data.authorization_url;
      } else {
        throw new Error("Failed to initiate Google OAuth");
      }
    } catch (error) {
      console.error("Google OAuth error:", error);
      toast.error("Không thể đăng nhập bằng Google. Vui lòng thử lại.");
      setLoading(null);
    }
  };

  const handleGitHubLogin = async () => {
    setLoading("github");
    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/github/login`);
      const data = await response.json();
      
      if (data.success && data.data.authorization_url) {
        window.location.href = data.data.authorization_url;
      } else {
        throw new Error("Failed to initiate GitHub OAuth");
      }
    } catch (error) {
      console.error("GitHub OAuth error:", error);
      toast.error("Không thể đăng nhập bằng GitHub. Vui lòng thử lại.");
      setLoading(null);
    }
  };

  return (
    <div className="space-y-3">
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Hoặc tiếp tục với
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <Button
          type="button"
          variant="outline"
          onClick={handleGoogleLogin}
          disabled={loading !== null}
          className="gap-2"
        >
          <Chrome className="w-4 h-4" />
          {loading === "google" ? "Đang xử lý..." : "Google"}
        </Button>

        <Button
          type="button"
          variant="outline"
          onClick={handleGitHubLogin}
          disabled={loading !== null}
          className="gap-2"
        >
          <Github className="w-4 h-4" />
          {loading === "github" ? "Đang xử lý..." : "GitHub"}
        </Button>
      </div>
    </div>
  );
};
```

#### B. OAuth Callback Handler

**File mới: `frontend/src/features/auth/pages/OAuthCallbackPage.tsx`**

```tsx
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "@/contexts/AuthContext";

const OAuthCallbackPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setAuthFromOAuth } = useAuth();

  useEffect(() => {
    const token = searchParams.get("token");
    const email = searchParams.get("email");

    if (token && email) {
      // Lưu token và email vào localStorage
      localStorage.setItem("career-compass-token", token);
      localStorage.setItem("career-compass-email", email);
      
      // Update AuthContext
      setAuthFromOAuth(email, token);
      
      toast.success("Đăng nhập thành công!");
      navigate("/solution", { replace: true });
    } else {
      toast.error("Đăng nhập thất bại. Vui lòng thử lại.");
      navigate("/login", { replace: true });
    }
  }, [searchParams, navigate, setAuthFromOAuth]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center space-y-4">
        <Loader2 className="w-12 h-12 animate-spin mx-auto text-accent" />
        <p className="text-muted-foreground">Đang xử lý đăng nhập...</p>
      </div>
    </div>
  );
};

export default OAuthCallbackPage;
```

#### C. Update AuthContext

**File: `frontend/src/shared/contexts/AuthContext.tsx`** - thêm method:

```tsx
type AuthContextType = {
  // ... existing fields
  setAuthFromOAuth: (email: string, token: string) => void;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  // ... existing code
  
  const setAuthFromOAuth = (email: string, token: string) => {
    setToken(token);
    setUser({ email });
  };

  const value = useMemo(
    () => ({ user, token, loading, login, signOut, setAuthFromOAuth }),
    [user, token, loading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

#### D. Update Auth Pages

**File: `frontend/src/features/auth/pages/AuthPage.tsx`** - thêm OAuth buttons:

```tsx
import { OAuthButtons } from "../components/OAuthButtons";

const AuthPage = () => {
  // ... existing code

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="glass-card rounded-2xl p-8 space-y-6">
          {/* ... existing email/password fields ... */}

          {/* Thêm OAuth buttons */}
          <OAuthButtons />

          {/* ... existing signup link ... */}
        </div>
      </motion.div>
    </div>
  );
};
```

**Tương tự cho `SignUpPage.tsx`**

#### E. Router Update

**File: `frontend/src/App.tsx` hoặc router file** - thêm route:

```tsx
import OAuthCallbackPage from "@/features/auth/pages/OAuthCallbackPage";

// Thêm route:
<Route path="/auth/callback" element={<OAuthCallbackPage />} />
```

#### F. Environment Variables

**File: `frontend/.env`**

```env
VITE_BACKEND_URL=http://localhost:9000
```

---

## 🔐 Security Considerations

### 1. CSRF Protection
- **Vấn đề**: OAuth callbacks dễ bị CSRF attacks
- **Giải pháp**: 
  - Lưu CSRF token vào Redis/session khi init OAuth
  - Verify token khi nhận callback
  - Set expiry 5 phút

### 2. State Parameter Validation
- Luôn kiểm tra `state` parameter khớp với giá trị đã gửi
- Implement một session store (Redis recommended)

### 3. Secure Token Storage
- **Frontend**: Lưu JWT trong httpOnly cookies thay vì localStorage (tránh XSS)
- **Backend**: Validate redirect URIs nghiêm ngặt

### 4. Email Verification
- Google: Email đã verified sẵn
- GitHub: Email có thể chưa verify → cần check `verified` field

---

## 📦 Database Migration (QUAN TRỌNG)

### Vấn đề hiện tại
- In-memory HashMap → **mất data khi restart**
- Không scale được
- Không thể lưu OAuth user info đầy đủ

### Giải pháp đề xuất: PostgreSQL + SQLx

#### Schema Design

**File: `backend/migrations/001_create_users_table.sql`**

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE auth_provider AS ENUM ('email', 'google', 'github');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    provider auth_provider NOT NULL DEFAULT 'email',
    provider_id VARCHAR(255),
    password_hash VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_email_provider CHECK (
        (provider = 'email' AND password_hash IS NOT NULL) OR
        (provider IN ('google', 'github') AND provider_id IS NOT NULL)
    ),
    
    -- Unique constraint cho OAuth providers
    UNIQUE(provider, provider_id)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_provider_id ON users(provider, provider_id);
```

#### Service Update

```rust
// backend/src/modules/auth/service.rs

use sqlx::PgPool;
use uuid::Uuid;

pub async fn find_or_create_oauth_user(
    pool: &PgPool,
    email: &str,
    name: Option<&str>,
    avatar_url: Option<&str>,
    provider_id: &str,
    provider: AuthProvider,
) -> Result<User, ApiError> {
    // Try to find existing user by provider_id
    if let Some(user) = sqlx::query_as!(
        User,
        r#"
        SELECT * FROM users 
        WHERE provider = $1 AND provider_id = $2
        "#,
        provider as AuthProvider,
        provider_id
    )
    .fetch_optional(pool)
    .await
    .map_err(|_| ApiError::Internal)? {
        return Ok(user);
    }

    // Try to find by email
    if let Some(user) = sqlx::query_as!(
        User,
        "SELECT * FROM users WHERE email = $1",
        email
    )
    .fetch_optional(pool)
    .await
    .map_err(|_| ApiError::Internal)? {
        // Email exists but different provider → link accounts
        return Ok(user);
    }

    // Create new user
    let user = sqlx::query_as!(
        User,
        r#"
        INSERT INTO users (email, name, avatar_url, provider, provider_id)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
        "#,
        email,
        name,
        avatar_url,
        provider as AuthProvider,
        provider_id
    )
    .fetch_one(pool)
    .await
    .map_err(|_| ApiError::Internal)?;

    Ok(user)
}
```

---

## 🚀 Implementation Roadmap

### Phase 1: Preparation (1-2 ngày)
- [ ] **P1.1** Setup PostgreSQL database
- [ ] **P1.2** Add database migrations
- [ ] **P1.3** Update User model với provider fields
- [ ] **P1.4** Migrate existing in-memory users to database
- [ ] **P1.5** Đăng ký Google OAuth app (Google Cloud Console)
- [ ] **P1.6** Đăng ký GitHub OAuth app (GitHub Settings)
- [ ] **P1.7** Add environment variables

### Phase 2: Backend OAuth Implementation (2-3 ngày)
- [ ] **P2.1** Add `oauth2` dependency vào Cargo.toml
- [ ] **P2.2** Implement `oauth.rs` module
- [ ] **P2.3** Implement OAuth handlers (Google)
- [ ] **P2.4** Implement OAuth handlers (GitHub)
- [ ] **P2.5** Add OAuth routes to router
- [ ] **P2.6** Test OAuth flow với Postman/Thunder Client
- [ ] **P2.7** Implement CSRF protection với Redis/session

### Phase 3: Frontend OAuth UI (1-2 ngày)
- [ ] **P3.1** Create `OAuthButtons` component
- [ ] **P3.2** Create `OAuthCallbackPage`
- [ ] **P3.3** Update `AuthContext` với `setAuthFromOAuth`
- [ ] **P3.4** Add OAuth buttons vào `AuthPage.tsx`
- [ ] **P3.5** Add OAuth buttons vào `SignUpPage.tsx`
- [ ] **P3.6** Add `/auth/callback` route
- [ ] **P3.7** Test UI flow end-to-end

### Phase 4: Testing & Polish (1 ngày)
- [ ] **P4.1** Test Google login flow
- [ ] **P4.2** Test GitHub login flow
- [ ] **P4.3** Test account linking khi email trùng
- [ ] **P4.4** Test error scenarios (denied permission, network errors)
- [ ] **P4.5** Add loading states và error messages
- [ ] **P4.6** Security audit (CSRF, redirect URIs, etc.)

### Phase 5: Documentation (0.5 ngày)
- [ ] **P5.1** Update README với OAuth setup instructions
- [ ] **P5.2** Document environment variables
- [ ] **P5.3** Create troubleshooting guide

---

## 🧪 Testing Strategy

### Unit Tests
```rust
// backend/src/modules/auth/tests.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_google_oauth_flow() {
        // Mock OAuth exchange
        // Verify user creation
        // Verify JWT generation
    }

    #[tokio::test]
    async fn test_github_oauth_flow() {
        // Similar to Google
    }

    #[tokio::test]
    async fn test_account_linking() {
        // Create user with email provider
        // Login via Google with same email
        // Verify accounts are linked
    }
}
```

### Integration Tests (Frontend)
```tsx
// frontend/src/features/auth/__tests__/oauth.test.tsx

describe("OAuth Flow", () => {
  it("should redirect to Google OAuth when clicking Google button", () => {
    // ...
  });

  it("should handle OAuth callback and save token", () => {
    // ...
  });
});
```

### Manual Testing Checklist
- [ ] Google OAuth happy path
- [ ] GitHub OAuth happy path
- [ ] User denies permission
- [ ] Invalid callback (tampered state)
- [ ] Network errors
- [ ] Email already exists with different provider

---

## 📚 External Resources

### Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project "CareerCompass"
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - Development: `http://localhost:9000/api/auth/google/callback`
   - Production: `https://yourdomain.com/api/auth/google/callback`
6. Copy Client ID và Client Secret vào `.env`

### GitHub OAuth Setup
1. Go to [GitHub Settings > Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in:
   - Application name: CareerCompass
   - Homepage URL: `http://localhost:5173`
   - Authorization callback URL: `http://localhost:9000/api/auth/github/callback`
4. Click "Register application"
5. Copy Client ID
6. Generate new Client Secret
7. Add vào `.env`

---

## ⚠️ Known Issues & Limitations

### Current Limitations
1. **No database** → cần migrate trước khi implement OAuth
2. **In-memory users** → không persist qua restarts
3. **No session management** → CSRF protection khó implement

### OAuth-Specific Challenges
1. **Email conflicts**: Nếu user có account Email và login qua Google cùng email → cần logic merge
2. **GitHub email privacy**: GitHub users có thể hide email → cần handle `null` email
3. **Account linking**: Nếu user đăng ký Email rồi login Google → need clear UX
4. **Token refresh**: Google tokens expire → cần implement refresh logic nếu cần long-lived sessions

---

## 💡 Recommendations

### Ưu tiên triển khai
1. **Phase 1 (Database)** là BƯỚC QUAN TRỌNG NHẤT → không nên skip
2. Implement Google OAuth trước (phổ biến hơn GitHub)
3. Implement CSRF protection ngay từ đầu (đừng để sau)

### Production Considerations
- Dùng Redis để lưu CSRF tokens (tránh in-memory)
- Enable rate limiting cho OAuth endpoints
- Log OAuth errors để debug
- Consider OAuth token refresh cho long-lived sessions
- Implement proper error pages (thay vì redirect về login với error query param)

### Nice-to-have Features
- [ ] Profile page hiển thị linked accounts
- [ ] Ability to unlink OAuth providers
- [ ] "Sign in with Google" trên mobile (deep links)
- [ ] OAuth scope customization
- [ ] Social profile import (avatar, name auto-fill)

---

## 📞 Implementation Support

Khi implement, refer to:
- [OAuth 2.0 RFC](https://datatracker.ietf.org/doc/html/rfc6749)
- [Google OAuth 2.0 Docs](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Docs](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)
- [Axum OAuth Example](https://github.com/tokio-rs/axum/tree/main/examples)
- [oauth2-rs Documentation](https://docs.rs/oauth2/)

---

**Tạo bởi**: GitHub Copilot  
**Ngày**: March 8, 2026  
**Version**: 1.0  
**Status**: 📝 Planning Phase
