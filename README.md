# Career Compass AI

Full-stack career assistance application built with React + Vite frontend, Rust backend, and Python NLP service.

## Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Backend**: Rust + Axum + JWT Auth + Template Engine (Tera) + Google Gemini AI
- **NLP Service**: Python 3.11 + FastAPI + Transformer Models
  - PhoBERT (Vietnamese NER)
  - BERT (English NER)
  - Sentence-Transformers (Semantic Similarity)
- **Features**: CV analysis, email generation, cover letter writing, AI assistant chatbot

##  NLP Models

The NLP service uses state-of-the-art transformer models for multilingual support:

### Vietnamese Processing (PhoBERT)
- **Model**: `vinai/phobert-base`
- **Purpose**: Named Entity Recognition for Vietnamese text
- **Capabilities**: Extracts skills, years of experience from Vietnamese CVs
- **Size**: ~400MB

### English Processing (BERT)
- **Model**: `bert-base-uncased`
- **Purpose**: Named Entity Recognition for English text  
- **Capabilities**: Extracts skills, years of experience from English CVs
- **Size**: ~440MB

### Semantic Similarity
- **Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Purpose**: Compute similarity between texts
- **Capabilities**: CV-JD matching, duplicate detection
- **Size**: ~470MB
- **Output**: Cosine similarity score (0.0 to 1.0)

### Template-Based Content Generation
The backend uses Tera templates for professional email and cover letter generation:
- **Languages**: Vietnamese (`vi`), English (`en`)
- **Styles**: Formal, Casual
- **Content Types**: Email Subject, Email Body, Cover Letter
- **Features**: Smart context extraction (name, skills, company, position, experience)

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Rust 1.70+ and Cargo
- **PostgreSQL 12+** (for database)
- Python 3.11+ with pip
- **Google Cloud account** (for Google OAuth - optional)
- **GitHub account** (for GitHub OAuth - optional)

### OAuth & Database Setup

🔐 **New!** OAuth authentication is now supported with Google and GitHub.

**For complete setup instructions including OAuth configuration:**

👉 **See [SETUP_GUIDE.md](./SETUP_GUIDE.md)** for step-by-step PostgreSQL and OAuth setup.

### Quick Steps:
- **Python 3.11+** (for NLP service)
- Google Gemini API key

### Setup

**1. NLP Service**:
```bash
cd nlp-service
python -m venv .venv311
.venv311\Scripts\activate  # Windows
# source .venv311/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

NLP Service runs on `http://127.0.0.1:8001`

**First Run Note**: Initial startup downloads 3 ML models (~900MB total). This may take 2-3 minutes.

**2. Backend**:
```bash
cd backend
cp .env.example .env
# Edit .env and add your GOOGLE_GEMINI_API_KEY
cargo run
```

Backend runs on `http://127.0.0.1:9000`

**3. Frontend**:
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:8080`

### Default Credentials

- Email: `admin@careercompass.local`
- Password: `admin123`

You can also register new accounts via the signup page.

## Project Structure

```
frontend/               # React frontend
  src/
    app/               # App entry and routing
    features/          # Feature modules (auth, cv-analysis, content-generation, marketing)
    shared/            # Shared components, contexts, hooks, utils
    legacy/            # Archived integrations reference

backend/               # Rust backend
  src/
    config/            # Settings management
    modules/           # Feature modules (auth, ai, content_generation, scoring)
      content_generation/
        template_engine.rs  # Template rendering with context extraction
        templates/          # Tera template files (12 templates)
    shared/            # Shared utilities (app state, errors, responses)
  templates/            # Email & cover letter templates (VI/EN, formal/casual)
  .env                  # Backend config (gitignored)
  .env.example          # Template for .env

nlp-service/            # Python NLP service
  app/
    main.py             # FastAPI app with all endpoints
    models.py           # ML model wrappers (PhoBERT, BERT, Similarity)
  tests/
    test_endpoints.py   # Comprehensive endpoint tests
  requirements.txt      # Python dependencies
```

## API Endpoints

### Auth
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT
- `POST /api/v1/auth/logout` - Logout (requires JWT)

### AI (all require JWT)
- `POST /api/v1/ai/chat-assistant` - Chat with AI career assistant

### Content Generation (all require JWT) - **Uses Templates**
- `POST /api/v1/content/generate-email` - Generate application email
- `POST /api/v1/content/generate-cover-letter` - Generate cover letter

### Scoring (all require JWT) - **Uses NLP Service**
- `POST /api/v1/scoring/analyze-cv` - Full CV analysis with scoring + email + cover letter

### NLP Service (Internal - Called by Backend)
- `GET /health` - Health check
- `POST /score-cv` - Score CV against JD (uses BERT/PhoBERT)
- `POST /ner/en` - English Named Entity Recognition (uses BERT)
- `POST /ner/vi` - Vietnamese Named Entity Recognition (uses PhoBERT)
- `POST /similarity` - Compute semantic similarity (uses Sentence-Transformers)

### Health
- `GET /health` - Backend health check

## Development

- **Frontend hot reload**: Vite dev server auto-reloads on file changes
- **Backend auto-rebuild**: Run `cargo watch -x run` for auto recompilation
- **NLP Service hot reload**: uvicorn `--reload` flag enables auto-reload
- **Backend logs**: Set `RUST_LOG=debug` in `backend/.env` for verbose logging

## Testing

### NLP Service Tests
```bash
cd nlp-service
pytest tests/test_endpoints.py -v
```

**Test Coverage**:
- Health endpoint
- CV scoring (English & Vietnamese)
- NER (English with BERT, Vietnamese with PhoBERT)
- Semantic similarity (similar & dissimilar texts)
- Performance benchmarks (< 3s response time)

## Troubleshooting

### NLP Service Issues

**Error: Models not found / downloading on every startup**
- Models are cached in `~/.cache/huggingface/`
- First download is ~900MB and takes 2-3 minutes
- Subsequent startups use cached models

**Error: ImportError - cannot import 'cached_download'**
- Cause: Incompatible sentence-transformers version
- Solution: Upgrade to sentence-transformers>=2.7.0
  ```bash
  pip install sentence-transformers==2.7.0 --upgrade
  ```

**Error: CUDA not available / torch errors**
- NLP service runs on CPU by default
- For GPU: Install CUDA-enabled PyTorch
- Current config uses CPU (sufficient for production)

**Slow NER/Similarity responses (> 5 seconds)**
- First request per model is slower (model loading)
- Subsequent requests are faster due to model caching
- Consider using quantized models for production

### Gemini API Errors

**Error: "Unknown name 'responseMimeType'"**
- Cause: Using unsupported field in v1 API
- Solution: Ensure `backend/src/modules/ai/gemini_client.rs` does NOT include `responseMimeType` in `generationConfig`

**Error: "models/gemini-1.5-flash-latest is not found for API version v1"**
- Cause: Wrong model name for v1 API  
- Solution: Use `gemini-2.5-flash` or other v1-compatible models
- Available models: `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-2.0-flash-001`

**Error: 502 Bad Gateway or 404 Not Found**
- Check that `GOOGLE_GEMINI_API_KEY` is valid
- Ensure using v1 API endpoint: `https://generativelanguage.googleapis.com/v1/models/...`
- Verify model name is compatible with v1 API (see above)

### Backend Build Issues

**Error: Linker error LNK1104 (Windows)**
- Cause: File locking by Windows Defender or another process
- Solution 1: Use `cargo check` to verify code compiles
- Solution 2: Run `cargo clean` before building
- Solution 3: Temporarily disable real-time protection

**Error: Address already in use**
- Another process is using port 9000
- Solution: Stop the process or change `BACKEND_PORT` in `backend/.env`

### Frontend Connection Issues

**CORS errors in browser console**
- Verify backend CORS settings in `backend/src/main.rs` allow your frontend origin
- Default allows: `http://localhost:8080` and `http://127.0.0.1:8080`

**401 Unauthorized on API calls**
- Check JWT token is being sent in `Authorization: Bearer <token>` header
- Token expires after 120 minutes (configurable via `JWT_EXPIRES_MINUTES` in backend `.env`)

## Production Build

**Frontend**:
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

**Backend**:
```bash
cd backend
cargo build --release
# Binary in backend/target/release/career_compass_backend
```

**NLP Service (Docker Recommended)**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## Performance Metrics

- **NER Latency**: < 3 seconds per request (including model inference)
- **Similarity Computation**: < 2 seconds per pair
- **Template Rendering**: < 50ms per template
- **Model Loading Time**: 20-40 seconds on startup (3 models)
- **Memory Usage (NLP Service)**: ~2.5GB with all models loaded

## Release Notes

See [RELEASE_NOTES.md](./RELEASE_NOTES.md) for detailed changelog and migration guide.

## License

MIT License - see LICENSE file for details
