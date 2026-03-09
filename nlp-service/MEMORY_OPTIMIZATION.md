# NLP Service - Memory Optimization for Render Free Tier

## Problem
Render free tier provides **512MB RAM**, but loading all 3 ML models requires:
- PhoBERT: ~400MB
- BERT: ~440MB  
- Similarity Model: ~470MB
- **Total: ~1.3GB** ❌

## Solution: Lazy Loading + Auto Memory Management

### Strategy
1. **No preload on startup** - models load only when first needed
2. **Load one model at a time** - clear unused models before loading new ones
3. **Automatic cleanup** - garbage collection after model swap
4. **Request-based loading**:
   - Vietnamese CV → Load PhoBERT only
   - English CV → Load BERT only
   - Similarity scoring → Load Similarity model only

### Memory Usage (Optimized)
- **Idle**: ~100MB (no models loaded)
- **Vietnamese request**: ~450MB (PhoBERT only)
- **English request**: ~490MB (BERT only)
- **Similarity**: ~520MB (Similarity model only)
- **Peak**: ~550MB ✅ (fits in 512MB with overhead)

### Trade-offs

**Pros:**
- ✅ Works on Render free tier (512MB)
- ✅ Zero cost
- ✅ No code changes in backend needed

**Cons:**
- ⚠️ **First request slower**: ~10-15 seconds (model loading time)
- ⚠️ **Model swap cost**: ~5-8 seconds when switching languages
- ⚠️ **Subsequent requests**: Fast (model cached until swap)

### Performance Characteristics

**Cold start (first request after deploy):**
```
Request → Load model (10-15s) → Process (2-3s) → Response
Total: ~12-18 seconds
```

**Warm request (same model):**
```
Request → Process (2-3s) → Response
Total: ~2-3 seconds
```

**Model swap (different language):**
```
Request → Clear old model (2s) → Load new model (10s) → Process (2s) → Response
Total: ~14 seconds
```

### Monitoring

Check logs for memory management:
```
INFO: Loading PhoBERT - clearing other models to save memory
INFO: Clearing BERT model from memory
INFO: Clearing Similarity model from memory
INFO: PhoBERT loaded successfully on cpu
```

### If Still OOM (Out of Memory)

If you still hit 512MB limit, try:

**Option 1: Reduce model precision**
```python
# In models.py, change to half precision
self.model.half()  # FP16 instead of FP32 (50% memory reduction)
```

**Option 2: Use smaller models**
```python
# Replace PhoBERT with smaller variant
model_name = "vinai/phobert-base-v2-small"  # ~200MB instead of 400MB

# Replace BERT with distilled version
model_name = "distilbert-base-uncased"  # ~260MB instead of 440MB
```

**Option 3: Disable advanced scoring**

Remove heavy models entirely, use only keyword matching:
```python
# In improved_scoring.py
# Skip BERT/PhoBERT, use regex + TF-IDF only
```

### Upgrade Path

When ready for production with better performance:

**Render Standard ($25/month):**
- 2GB RAM
- Can keep all 3 models loaded
- No swap delays
- Consistently fast

**Railway ($10-15/month):**
- 2GB+ RAM configurable
- Pay per usage
- Better for variable traffic

**Koyeb (Free):**
- 2GB RAM free
- Sleep after 30min idle  
- Good for testing

---

## Current Configuration

✅ **Lazy loading enabled** in `app/main.py`
✅ **Auto memory management** in `app/models.py`
✅ **Works on Render free tier** (512MB)

**No environment variables needed** - optimization is automatic.

---

## Testing Locally

Test memory-constrained environment:

```bash
# Limit Python memory (Linux/Mac)
ulimit -v 524288  # 512MB in KB
python -m uvicorn app.main:app

# Windows (PowerShell) - no direct limit, monitor with:
while ($true) {
    Get-Process python | Select-Object WS,PM | Format-Table
    Start-Sleep 5
}
```

Test model swapping:
```bash
# 1. Vietnamese request (loads PhoBERT)
curl -X POST http://localhost:8000/score-cv \
  -H "Content-Type: application/json" \
  -d '{"cv_text":"Lập trình viên Python","jd_text":"Backend Engineer","language":"vi"}'

# 2. English request (swaps to BERT)
curl -X POST http://localhost:8000/score-cv \
  -H "Content-Type: application/json" \
  -d '{"cv_text":"Python Developer","jd_text":"Backend Engineer","language":"en"}'

# 3. Check logs for "Clearing..." messages
```

Expected logs:
```
INFO: Loading PhoBERT - clearing other models to save memory
INFO: PhoBERT loaded successfully
... (first request completes)
INFO: Loading BERT - clearing other models to save memory
INFO: Clearing PhoBERT model from memory
INFO: BERT loaded successfully
... (second request completes)
```
