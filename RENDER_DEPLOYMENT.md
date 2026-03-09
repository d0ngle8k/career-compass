# Render Deployment Guide

## What I Fixed

### 1. NLP Service Dependency Issue ✅
**Problem:** `torch==2.1.2` not compatible with Python 3.14  
**Solution:** Updated `nlp-service/requirements.txt` to modern versions:
- `torch==2.10.0` (Python 3.14 compatible)
- `transformers==4.48.0`
- `sentence-transformers==3.5.0`
- `scikit-learn==1.6.1`

Added `nlp-service/runtime.txt` to pin Python 3.11.10 (more stable for ML workloads)

### 2. Backend CORS Auto-Configuration ✅
**Problem:** Hardcoded frontend URLs in `backend/src/main.rs`  
**Solution:** CORS now automatically allows the URL from `FRONTEND_URL` environment variable
- Keeps localhost origins for development
- Dynamically adds production frontend URL from env

### 3. Render Blueprint Created ✅
Created `render.yaml` for one-click deployment of all services

---

## Deploy to Render (Two Methods)

### Method 1: Blueprint (Recommended - One Click)

1. Push your changes to GitHub:
```bash
git add .
git commit -m "fix: update dependencies for Render deployment"
git push
```

2. Go to [Render Dashboard](https://dashboard.render.com/)

3. Click **"New"** → **"Blueprint"**

4. Connect your GitHub repo `d0ngle8k/career-compass-ai`

5. Render will detect `render.yaml` and create all 4 services:
   - `career-compass-db` (PostgreSQL)
   - `career-compass-nlp` (Python NLP service)
   - `career-compass-backend` (Rust Axum API)
   - `career-compass-frontend` (Static site)

6. **Set required secrets** in each service dashboard:
   - Backend:
     - `ADMIN_PASSWORD` (choose a secure password)
     - `GOOGLE_GEMINI_API_KEY` (your Gemini API key)
     - Optional OAuth: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`
   
7. Deploy!

### Method 2: Manual (Step-by-Step)

#### Step 1: Deploy PostgreSQL Database
1. Dashboard → **New** → **PostgreSQL**
2. Name: `career-compass-db`
3. Database: `career_compass`
4. Create
5. Copy **Internal Database URL** for backend

#### Step 2: Deploy NLP Service
1. **New** → **Web Service**
2. Connect repo, select branch `main`
3. Configure:
   - **Name:** `career-compass-nlp`
   - **Region:** Singapore (or closest to you)
   - **Root Directory:** `nlp-service`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Starter (minimum - ML models need RAM)
4. **Environment:** 
   - `PYTHON_VERSION=3.11.10` (auto-detected from runtime.txt)
5. Create Service
6. Wait for build (first time downloads ~1GB models, takes 5-10 min)
7. Copy service URL: `https://career-compass-nlp.onrender.com`

Test: `curl https://career-compass-nlp.onrender.com/health`  
Should return: `{"status":"ok"}`

#### Step 3: Deploy Backend
1. **New** → **Web Service**
2. Configure:
   - **Name:** `career-compass-backend`
   - **Root Directory:** `backend`
   - **Runtime:** Rust
   - **Build Command:** `cargo build --release`
   - **Start Command:** `BACKEND_HOST=0.0.0.0 BACKEND_PORT=$PORT ./target/release/career_compass_backend`
   - **Instance Type:** Starter
3. **Environment Variables:**
```bash
RUST_LOG=info
JWT_SECRET=<generate-a-strong-random-secret-at-least-32-chars>
JWT_EXPIRES_MINUTES=120
ADMIN_EMAIL=admin@careercompass.local
ADMIN_PASSWORD=<choose-secure-password>
GOOGLE_GEMINI_API_KEY=<your-gemini-api-key>
GOOGLE_GEMINI_MODEL=gemini-2.5-flash
NLP_SERVICE_URL=https://career-compass-nlp.onrender.com
NLP_TIMEOUT_MS=10000
DATABASE_URL=<paste-your-postgres-internal-url>
FRONTEND_URL=https://career-compass-frontend.onrender.com
```

Optional OAuth (leave empty if not using):
```bash
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=https://career-compass-backend.onrender.com/api/v1/auth/google/callback
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_REDIRECT_URI=https://career-compass-backend.onrender.com/api/v1/auth/github/callback
```

4. Create Service
5. Copy URL: `https://career-compass-backend.onrender.com`

Test: `curl https://career-compass-backend.onrender.com/health`

#### Step 4: Deploy Frontend
1. **New** → **Static Site**
2. Configure:
   - **Name:** `career-compass-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
3. **Environment Variables:**
```bash
VITE_BACKEND_URL=https://career-compass-backend.onrender.com
```
4. Create Site
5. Once deployed, go to **Settings** → add redirect rule:
   - **Source:** `/*`
   - **Destination:** `/index.html`
   - **Action:** Rewrite

---

## Post-Deployment Steps

### 1. Update OAuth Provider Callbacks (if using OAuth)

**Google Cloud Console:**
- Go to your OAuth app
- Add authorized redirect URI: `https://career-compass-backend.onrender.com/api/v1/auth/google/callback`

**GitHub Developer Settings:**
- Go to your OAuth app
- Update callback URL: `https://career-compass-backend.onrender.com/api/v1/auth/github/callback`

### 2. Test Your Deployment

1. **Health Checks:**
   - NLP: `https://career-compass-nlp.onrender.com/health` → `{"status":"ok"}`
   - Backend: `https://career-compass-backend.onrender.com/health` → `{"status":"healthy"}`

2. **Frontend:**
   - Visit: `https://career-compass-frontend.onrender.com`
   - Try login/register
   - Test protected pages (`/solution`, `/write-mail`, `/write-cover-letter`)

3. **End-to-End:**
   - Upload a CV and JD, run scoring (tests backend → NLP integration)
   - Generate email/cover letter
   - Test chatbot

---

## Important Notes

### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- First request after sleep takes ~50 seconds
- **Solution:** Upgrade to paid tier ($7/month per service) for always-on

### Build Times
- Backend (Rust): First build ~10-15 minutes
- NLP Service: First build ~5-10 minutes (downloads ML models)
- Frontend: ~2-3 minutes

### Scaling Recommendations
1. Start with **Starter** instance for backend and NLP
2. Monitor memory usage in Render dashboard
3. NLP service may need **Standard** if handling many concurrent requests
4. Frontend static site doesn't need upgrade

### Troubleshooting

**Backend build fails:**
- Check `DATABASE_URL` is set correctly
- Ensure all required env vars are present

**NLP service timeout:**
- First request after sleep is slow (model loading)
- Increase `NLP_TIMEOUT_MS` to 30000 for cold starts
- Consider paid tier to avoid spin-down

**CORS errors:**
- Verify `FRONTEND_URL` in backend matches your frontend domain exactly
- Check browser console for actual origin being blocked
- Backend logs will show "Adding production frontend origin: ..."

**OAuth not working:**
- Verify callback URLs match exactly in provider dashboards
- Check `FRONTEND_URL` redirects back correctly
- Test with `http://localhost:5173` first before production

---

## Environment Variables Summary

| Service | Variable | Required | Example |
|---------|----------|----------|---------|
| Backend | JWT_SECRET | ✅ | auto-generated or custom |
| Backend | ADMIN_PASSWORD | ✅ | your-secure-password |
| Backend | GOOGLE_GEMINI_API_KEY | ✅ | AIza... |
| Backend | DATABASE_URL | ✅ | postgresql://... |
| Backend | NLP_SERVICE_URL | ✅ | https://...nlp.onrender.com |
| Backend | FRONTEND_URL | ✅ | https://...frontend.onrender.com |
| Backend | GOOGLE_CLIENT_ID | ❌ | optional OAuth |
| Backend | GOOGLE_CLIENT_SECRET | ❌ | optional OAuth |
| Backend | GITHUB_CLIENT_ID | ❌ | optional OAuth |
| Backend | GITHUB_CLIENT_SECRET | ❌ | optional OAuth |
| Frontend | VITE_BACKEND_URL | ✅ | https://...backend.onrender.com |

---

## Next Steps After Successful Deploy

1. **Custom Domain** (optional):
   - Add custom domain in Render dashboard
   - Update CORS/OAuth accordingly

2. **Monitoring:**
   - Set up Render health check alerts
   - Monitor logs for errors

3. **Backup:**
   - Enable Render Postgres automated backups

4. **Performance:**
   - Consider Redis for caching if needed
   - Upgrade to paid tier for production traffic
