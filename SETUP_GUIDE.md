# Career Compass AI - OAuth & Database Setup Guide

## 🎯 Quick Start Overview

This guide walks you through setting up PostgreSQL database and OAuth authentication (Google & GitHub) for Career Compass AI.

**Prerequisites:**
- PostgreSQL 12+ installed
- Google Cloud Console account (for Google OAuth)
- GitHub account (for GitHub OAuth)
- Node.js 18+ and Rust 1.70+

**Estimated Setup Time:** 30-45 minutes

---

## 📦 Step 1: PostgreSQL Database Setup

### 1.1 Install PostgreSQL

**Windows:**
```powershell
# Download from https://www.postgresql.org/download/windows/
# Or use Chocolatey:
choco install postgresql

# Start PostgreSQL service
net start postgresql-x64-14
```

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 1.2 Create Database

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Create database
CREATE DATABASE career_compass;

# Create user (optional, recommended for production)
CREATE USER career_user WITH ENCRYPTED PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE career_compass TO career_user;

# Exit psql
\q
```

### 1.3 Verify Connection

```bash
# Test connection
psql -U postgres -d career_compass -c "SELECT version();"
```

---

## 🔑 Step 2: Google OAuth Setup

### 2.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a Project"** → **"New Project"**
3. Enter project name: `CareerCompassAI`
4. Click **"Create"**

### 2.2 Enable Google+ API

1. In your project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google+ API"**
3. Click **"Enable"**

### 2.3 Create OAuth 2.0 Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `Career Compass AI`
   - User support email: your email
   - Developer contact: your email
   - Scopes: Add `/auth/userinfo.email` and `/auth/userinfo.profile`
   - Test users: Add your email
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: `Career Compass Web`
   - Authorized redirect URIs:
     - Development: `http://localhost:9000/api/v1/auth/google/callback`
     - Production: `https://yourdomain.com/api/v1/auth/google/callback`
5. Click **"Create"**
6. **Important:** Copy your **Client ID** and **Client Secret** - you'll need these for `.env`

### 2.4 Example Credentials

```
Client ID: 123456789-abcdefg.apps.googleusercontent.com
Client Secret: GOCSPX-abc123def456ghi789
```

---

## 🐙 Step 3: GitHub OAuth Setup

### 3.1 Create GitHub OAuth App

1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Click **"OAuth Apps"** → **"New OAuth App"**

### 3.2 Configure OAuth App

Fill in the following:

- **Application name:** `Career Compass AI`
- **Homepage URL:** `http://localhost:5173` (development) or `https://yourdomain.com` (production)
- **Application description:** `AI-powered CV analysis and career guidance platform`
- **Authorization callback URL:** `http://localhost:9000/api/v1/auth/github/callback`

Click **"Register application"**

### 3.3 Generate Client Secret

1. After registration, you'll see your **Client ID**
2. Click **"Generate a new client secret"**
3. **Important:** Copy the secret immediately - it won't be shown again!

### 3.4 Example Credentials

```
Client ID: Iv1.a1b2c3d4e5f6g7h8
Client Secret: 1234567890abcdef1234567890abcdef12345678
```

---

## ⚙️ Step 4: Configure Environment Variables

### 4.1 Backend Configuration

Create/update `backend/.env` file:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/career_compass

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:9000/api/v1/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:9000/api/v1/auth/github/callback

# Frontend URL
FRONTEND_URL=http://localhost:5173

# Other required variables (keep existing)
JWT_SECRET=replace-with-a-random-secret-at-least-32-characters
ADMIN_EMAIL=admin@careercompass.local
ADMIN_PASSWORD=admin123
GOOGLE_GEMINI_API_KEY=your-gemini-api-key
```

**Important Notes:**
- Replace `postgres:postgres` in DATABASE_URL with your actual username:password
- Replace OAuth credentials with your actual values from Steps 2 & 3
- For production, update all URLs to your domain
- Passwords are stored as Argon2 hashes (not plain text)

### 4.2 Frontend Configuration

`frontend/.env` should already have:

```env
VITE_BACKEND_URL=http://127.0.0.1:9000
```

---

## 🚀 Step 5: Build and Run

### 5.1 Install Dependencies

```bash
# Backend (Rust)
cd backend
cargo build

# Frontend (Node.js)
cd ../frontend
npm install
```

### 5.2 Run Database Migrations

Migrations run automatically when the backend starts. The first time you run the backend, it will:
- Create the `users` table
- Set up indexes
- Insert default admin user

### 5.3 Start Services

**Terminal 1 - Backend:**
```bash
cd backend
cargo run
```

You should see:
```
INFO backend: Connecting to database...
INFO backend: Database connection pool created successfully
INFO backend: Running database migrations...
INFO backend: Database migrations completed successfully
INFO backend: Templates initialized successfully
INFO backend: backend listening on http://127.0.0.1:9000
```

**Terminal 2 - NLP Service:**
```bash
cd nlp-service
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## ✅ Step 6: Test OAuth Integration

### 6.1 Test Google OAuth

1. Open browser to `http://localhost:5173/auth`
2. Click **"Google"** button
3. You should be redirected to Google consent screen
4. Sign in with your Google account
5. Grant permissions
6. You should be redirected back to `http://localhost:5173/solution`
7. Check browser localStorage - you should see:
   - `career-compass-token`
   - `career-compass-email`

### 6.2 Test GitHub OAuth

1. Go to `http://localhost:5173/auth`
2. Click **"GitHub"** button
3. Authorize the app
4. Should redirect back and log you in

### 6.3 Verify Database

Check that user was created:

```bash
psql -U postgres -d career_compass

SELECT id, email, name, provider, created_at FROM users;
```

You should see your OAuth user(s) listed.

---

## ✉️ Step 7: EmailJS Setup (Contact Form)

Contact page now sends user feedback via EmailJS with exactly 3 fields:
- `name`
- `email`
- `text`

### 7.1 Create EmailJS Service & Template

1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/)
2. Create an Email Service (Gmail/Outlook/SMTP)
3. Create an Email Template and include variables:
   - `{{name}}`
   - `{{email}}`
   - `{{text}}`
4. Copy the following values:
   - Service ID
   - Template ID
   - Public Key

### 7.2 Configure Frontend Environment

Create/update `frontend/.env`:

```env
VITE_BACKEND_URL=http://127.0.0.1:9000
VITE_EMAILJS_SERVICE_ID=your_service_id
VITE_EMAILJS_TEMPLATE_ID=your_template_id
VITE_EMAILJS_PUBLIC_KEY=your_public_key
```

You can also copy from `frontend/.env.example` and fill real values.

### 7.3 Test Contact Form

1. Start frontend: `cd frontend && npm run dev`
2. Open `/contact`
3. Fill `Họ tên`, `Email`, `Nội dung`
4. Submit and verify email arrives at your configured inbox

If config is missing, UI will show a clear `EmailJS is not configured` error toast.

---

## 🐛 Troubleshooting

### Issue: "Failed to create database pool"

**Cause:** PostgreSQL not running or DATABASE_URL incorrect

**Fix:**
```bash
# Check PostgreSQL is running
# Windows:
net start postgresql-x64-14

# macOS:
brew services start postgresql@14

# Linux:
sudo systemctl status postgresql

# Test connection manually:
psql -U postgres -d career_compass
```

### Issue: "Google OAuth not configured"

**Cause:** GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is empty

**Fix:** 
- Verify you added credentials to `backend/.env`
- Restart backend after updating .env file
- Check for typos in environment variable names

### Issue: "Failed to exchange authorization code"

**Cause:** Redirect URI mismatch

**Fix:**
- Google Console: Verify redirect URI exactly matches: `http://localhost:9000/api/v1/auth/google/callback`
- GitHub Settings: Verify callback URL exactly matches: `http://localhost:9000/api/v1/auth/github/callback`
- No trailing slashes
- Use `http://` not `https://` for localhost

### Issue: "OAuth loop" (keeps redirecting back to login)

**Cause:** Frontend not receiving/storing token properly

**Fix:**
- Open browser DevTools (F12) → Console
- Check for JavaScript errors
- Verify localStorage has `career-compass-token` after OAuth callback
- Check Network tab for failed API requests

### Issue: Migration errors

**Cause:** Database schema already exists or permission issues

**Fix:**
```bash
# Drop and recreate database
psql -U postgres

DROP DATABASE career_compass;
CREATE DATABASE career_compass;
\q

# Restart backend to re-run migrations
```

---

## 🔒 Security Best Practices

### For Production Deployment:

1. **Use HTTPS everywhere:**
   ```env
   GOOGLE_REDIRECT_URI=https://yourdomain.com/api/v1/auth/google/callback
   GITHUB_REDIRECT_URI=https://yourdomain.com/api/v1/auth/github/callback
   FRONTEND_URL=https://yourdomain.com
   ```

2. **Use strong secrets:**
   ```bash
   # Generate secure JWT secret
   openssl rand -base64 32
   ```

3. **Use environment-specific credentials:**
   - Create separate OAuth apps for dev/staging/production
   - Never commit `.env` files to git
   - Use secret management (AWS Secrets Manager, HashiCorp Vault, etc.)

4. **Database security:**
   - Create dedicated database user (not postgres superuser)
   - Use strong password
   - Enable SSL connection
   - Restrict network access

5. **OAuth security:**
   - CSRF `state` validation is enabled for OAuth callbacks
   - Regularly rotate client secrets
   - Review OAuth scopes - only request what you need
   - Monitor for suspicious login attempts

6. **Secret rotation policy:**
   - Rotate `JWT_SECRET` immediately if it was shared in logs/chat
   - Rotate `GOOGLE_CLIENT_SECRET` and `GITHUB_CLIENT_SECRET` from provider dashboards if exposed
   - Restart backend after every secret rotation

---

## 📊 Testing Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `career_compass` created
- [ ] Backend connects to database successfully
- [ ] Migrations run without errors
- [ ] Google OAuth app created
- [ ] Google OAuth credentials in `.env`
- [ ] GitHub OAuth app created
- [ ] GitHub OAuth credentials in `.env`
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can register with email/password
- [ ] Can login with email/password
- [ ] Can login with Google OAuth
- [ ] Can login with GitHub OAuth
- [ ] User appears in database after OAuth login
- [ ] Token stored in localStorage
- [ ] Protected routes accessible after login

---

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check backend logs for detailed error messages
2. Check browser console for frontend errors
3. Verify all environment variables are set correctly
4. Ensure all services (PostgreSQL, backend, NLP, frontend) are running
5. Review the [OAUTH_IMPLEMENTATION_PLAN.md](./OAUTH_IMPLEMENTATION_PLAN.md) for technical details

---

## 📝 Quick Reference

### Database Connection String Format
```
postgresql://[user[:password]@][host][:port][/dbname]
```

### OAuth Callback URLs
```
Google:  http://localhost:9000/api/v1/auth/google/callback
GitHub:  http://localhost:9000/api/v1/auth/github/callback
```

### Required Environment Variables
```
DATABASE_URL
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET
JWT_SECRET
```

---

**Setup complete!** 🎉

You now have a fully functional OAuth authentication system with Google and GitHub login.
