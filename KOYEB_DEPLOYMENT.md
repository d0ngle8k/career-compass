# Deploy NLP Service lên Koyeb (Free 2GB RAM)

## Tại sao Koyeb?
- ✅ **FREE**: 2GB RAM, 2 vCPU (đủ cho 3 ML models)
- ✅ **Auto-deploy** từ GitHub
- ✅ **HTTPS** tự động
- ⚠️ **Sleep** sau 30 phút idle (wake up khi có request ~5-10s)

## Bước 1: Đăng ký Koyeb

1. Vào https://app.koyeb.com/auth/signup
2. Sign up bằng **GitHub account** (nhanh nhất)
3. Confirm email → vào Dashboard

## Bước 2: Deploy NLP Service

### Option A: Deploy từ GitHub (Khuyến nghị)

1. **Tạo service mới:**
   - Vào https://app.koyeb.com/apps
   - Click **"Create App"**

2. **Configure deployment:**
   
   **GitHub Repository:**
   - Select **"GitHub"** 
   - Authorize Koyeb access repository
   - Choose: `d0ngle8k/career-compass-ai`
   - Branch: `main`
   - **Root directory**: `nlp-service`

   **Builder:**
   - Builder: **Buildpack**
   - Build command: `pip install -r requirements.txt`
   - Run command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

   **Instance:**
   - Region: **Frankfurt (FRA)** hoặc **Washington DC (WAS)**
   - Instance type: **Free** (2GB RAM, 2 vCPU)
   - Auto-scaling: Off

   **Exposure:**
   - Port: `8000` (Koyeb sẽ map từ $PORT)
   - Protocol: HTTP
   - Public: ✅

   **Environment Variables:**
   - `PYTHON_VERSION`: `3.11.10`

3. **Deploy:**
   - App name: `career-compass-nlp`
   - Click **"Deploy"**

4. **Đợi deployment** (~5-8 phút):
   ```
   ✓ Building... (2-3 phút - download dependencies)
   ✓ Uploading... (1-2 phút)
   ✓ Deploying... (2-3 phút - load ML models)
   ✓ Healthy ✅
   ```

### Option B: Deploy từ Docker (Advanced)

Tạo `nlp-service/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Rồi deploy:
- Builder: **Docker**
- Dockerfile: `nlp-service/Dockerfile`

## Bước 3: Lấy Public URL

Sau khi deploy xong:

1. Vào **App details** → **Domains**
2. Copy **Public URL**: `https://career-compass-nlp-xxxxxx.koyeb.app`

## Bước 4: Update Backend Environment Variable

### Nếu Backend đang ở Render:

1. Vào Render Dashboard → `career-compass-backend`
2. Environment → sửa:
   ```
   NLP_SERVICE_URL=https://career-compass-nlp-xxxxxx.koyeb.app
   ```
3. Save → Redeploy backend

### Nếu Backend chạy local:

Update `backend/.env`:
```env
NLP_SERVICE_URL=https://career-compass-nlp-xxxxxx.koyeb.app
```

## Bước 5: Test NLP Service

```bash
# Health check
curl https://career-compass-nlp-xxxxxx.koyeb.app/health

# Test scoring
curl -X POST https://career-compass-nlp-xxxxxx.koyeb.app/score-cv \
  -H "Content-Type: application/json" \
  -d '{
    "cv_text": "Python Developer with 3 years experience in Django and FastAPI",
    "jd_text": "Looking for Python Backend Engineer",
    "language": "en"
  }'
```

Expected response:
```json
{
  "success": true,
  "data": {
    "score": 75.5,
    "strengths": ["Python experience", "FastAPI knowledge"],
    "weaknesses": ["Missing DevOps skills"],
    "improvement_tips": ["Add Docker, Kubernetes"]
  }
}
```

## Bước 6: Monitor & Logs

1. **View logs:**
   - Koyeb Dashboard → App → **Logs** tab
   - Real-time logs hiển thị model loading:
     ```
     INFO:app.main:Preloading ML models...
     INFO:app.models:Loading PhoBERT model: vinai/phobert-base
     INFO:app.main:PhoBERT loaded successfully
     INFO:app.main:BERT loaded successfully
     INFO:app.main:Similarity model loaded successfully
     INFO:app.main:NLP service ready
     ```

2. **Monitor metrics:**
   - **Metrics** tab: CPU, RAM usage
   - Expect: ~1.5-1.8GB RAM khi models loaded

3. **Auto-sleep behavior:**
   - Sau 30 phút không request → service sleep
   - Request mới → wake up trong ~5-10 giây
   - First request sau wake up sẽ hơi chậm

## Troubleshooting

### Out of Memory (>2GB)

Nếu vẫn OOM, giảm memory bằng cách load models on-demand:

**Sửa `nlp-service/app/main.py`:**
```python
@app.on_event("startup")
async def startup_event():
    """Don't preload - load on first request"""
    logger.info("NLP service ready (lazy loading mode)")
    # Comment out preload calls
```

### Build quá chậm

Download PyTorch (2.10.0) ~800MB nên build lâu. Sau lần đầu Koyeb cache dependencies.

### Service unhealthy

Check logs:
```bash
# View last 100 lines
koyeb logs career-compass-nlp --tail 100
```

## So sánh Render vs Koyeb

| Feature | Render (Free) | Koyeb (Free) |
|---------|--------------|--------------|
| RAM | 512MB ❌ | 2GB ✅ |
| CPU | Shared | 2 vCPU |
| Sleep | 15min idle | 30min idle |
| Region | Singapore ✅ | EU/US |
| Build time | ~3-4min | ~5-8min |

## Deployment Architecture (Hybrid)

```
┌─────────────────────────────────────┐
│  Frontend (Render/Vercel)           │
│  Static Site                        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Backend (Render)                   │
│  Rust Axum + PostgreSQL             │
│  512MB                              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  NLP Service (Koyeb) ✅             │
│  Python + ML Models                 │
│  2GB RAM                            │
└─────────────────────────────────────┘
```

## Next Steps

1. ✅ Deploy NLP lên Koyeb
2. ✅ Update `NLP_SERVICE_URL` trong backend
3. Test full-stack:
   - Frontend → Backend → NLP (Koyeb)
   - Verify CV scoring works
4. Production:
   - Setup custom domain (optional)
   - Monitor cold starts
   - Consider upgrade nếu cần 24/7 uptime
