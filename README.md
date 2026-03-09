# Career Compass AI

Career Compass AI is a full-stack platform for CV analysis, JD matching, and AI-assisted job application content generation.

## System Architecture

The project is split into 3 deployable services:

1. `frontend` (React + Vite)
- User-facing web app.
- Handles authentication UI, CV/JD submission, result display, and content generation screens.

2. `backend` (Rust + Axum)
- Main API gateway and business logic.
- Handles auth, JWT, OAuth (Google/GitHub), CV analysis orchestration, template-based content generation, and DB access.

3. `nlp-service` (Python + FastAPI)
- NLP scoring and extraction service.
- Runs multilingual models (PhoBERT/BERT/Sentence-Transformers) in lazy-loading mode to fit low-memory environments.

Data flow:

1. User interacts with `frontend`.
2. `frontend` calls `backend` APIs.
3. `backend` calls `nlp-service` for CV/JD analysis.
4. `backend` stores user/auth data in PostgreSQL and returns processed results to `frontend`.

## Tech Stack

- Frontend: React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui
- Backend: Rust, Axum, SQLx, PostgreSQL, JWT, OAuth2, Tera templates
- NLP: Python 3.11, FastAPI, transformers, sentence-transformers, torch
- Deployment: Render (Blueprint via `render.yaml`)

## Repository Structure

```text
career-compass-ai/
|-- backend/
|   |-- .cargo/config.toml            # Rust build settings
|   |-- .env.example                  # Backend env template
|   |-- .sqlx/                        # SQLx offline query metadata
|   |-- migrations/                   # PostgreSQL migrations
|   |-- src/
|   |   |-- config/
|   |   |   |-- mod.rs
|   |   |   `-- settings.rs           # Environment/config loader
|   |   |-- modules/
|   |   |   |-- ai/                   # Gemini chat assistant module
|   |   |   |-- auth/                 # JWT + OAuth + user auth
|   |   |   |-- content_generation/   # Email/Cover letter generation
|   |   |   |-- health/               # Health endpoints
|   |   |   |-- scoring/              # CV/JD scoring orchestration
|   |   |   `-- mod.rs
|   |   |-- shared/                   # Shared API/database utilities
|   |   `-- main.rs                   # Backend bootstrap and router
|   |-- templates/                    # Tera templates (EN/VI, multi-style)
|   |-- Cargo.toml
|   `-- Cargo.lock
|
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- app/                      # App shell and entry point
|   |   |-- components/               # Reusable UI components
|   |   |-- contexts/                 # Global context providers
|   |   |-- features/                 # Feature-driven pages/modules
|   |   |-- hooks/                    # Shared React hooks
|   |   |-- legacy/                   # External integration references
|   |   |-- lib/                      # General utility helpers
|   |   |-- pages/                    # Top-level route pages
|   |   `-- shared/                   # Shared components/libs/contexts
|   |-- package.json
|   |-- vite.config.ts
|   `-- vitest.config.ts
|
|-- nlp-service/
|   |-- app/
|   |   |-- main.py                   # FastAPI entrypoint
|   |   |-- models.py                 # Lazy model loading + memory cleanup
|   |   |-- advanced_scoring.py
|   |   |-- enhanced_scoring.py
|   |   `-- improved_scoring.py
|   |-- scripts/                      # NLP experimentation/support scripts
|   |-- test_data/                    # NLP test fixtures
|   |-- tests/                        # NLP endpoint tests
|   |-- requirements.txt
|   |-- runtime.txt                   # Python runtime for Render
|   `-- Dockerfile
|
|-- render.yaml                       # Render Blueprint (db + services)
|-- SETUP_GUIDE.md                    # Full local setup guide
|-- RENDER_DEPLOYMENT.md              # Render deployment notes
|-- KOYEB_DEPLOYMENT.md               # Koyeb deployment notes
|-- SELF_HOST_GUIDE.md                # Self-host instructions
`-- README.md
```

## Core Backend Modules

- `modules/auth`: register/login, JWT issuance/validation, OAuth flows.
- `modules/scoring`: coordinates CV/JD analysis and NLP service calls.
- `modules/content_generation`: builds email/cover-letter output from templates.
- `modules/ai`: Gemini-powered conversational assistant.

## Environment Variables

Backend critical vars:

- `DATABASE_URL`
- `JWT_SECRET`
- `BACKEND_HOST`
- `BACKEND_PORT`
- `NLP_SERVICE_URL`
- `GOOGLE_GEMINI_API_KEY`

NLP critical vars:

- `PYTHON_VERSION` (Render)

Frontend critical vars:

- `VITE_BACKEND_URL`
- `VITE_EMAILJS_SERVICE_ID` (if contact form enabled)
- `VITE_EMAILJS_TEMPLATE_ID`
- `VITE_EMAILJS_PUBLIC_KEY`

## Local Development

Run services in this order.

1. NLP service

```bash
cd nlp-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

2. Backend

```bash
cd backend
cargo run
```

3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Default local URLs:

- Frontend: `http://localhost:8080`
- Backend: `http://localhost:9000`
- NLP service: `http://localhost:8001`

## Deployment

Render is the primary deployment target via `render.yaml`:

- PostgreSQL database service
- Rust backend web service
- Python NLP web service
- Static frontend web service

See `RENDER_DEPLOYMENT.md` for operational troubleshooting.

## Notes

- NLP models are loaded lazily to reduce memory usage on low-tier instances.
- SQLx offline metadata is committed under `backend/.sqlx/`.
- Root-level ad-hoc test artifacts were removed to keep production repository clean.
