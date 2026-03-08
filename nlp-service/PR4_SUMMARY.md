# PR-4: Vietnamese NER with PhoBERT - Implementation Summary

## ✅ Completed Tasks

### 1. ML Dependencies Added
- **torch==2.1.2** (192.3 MB) - PyTorch deep learning framework
- **transformers==4.36.2** (8.2 MB) - Hugging Face Transformers library  
- **sentencepiece==0.1.99** - Tokenizer for PhoBERT
- **numpy<2.0** - Pinned to avoid compatibility issues with PyTorch 2.1

### 2. PhoBERT Model Implementation
Created `nlp-service/app/models.py` with:
- **PhoBERTModel class**: Vietnamese BERT wrapper
  - Model: `vinai/phobert-base` (135M parameters)
  - Lazy loading with singleton pattern
  - GPU/CPU auto-detection
  - Contextual embeddings extraction
  - Enhanced skill extraction with word boundary matching
  - Years of experience extraction (Vietnamese + English patterns)
  
- **BERTModel class**: English BERT placeholder (PR-5)
  - Model: `bert-base-uncased`  
  - Same interface as PhoBERT for consistency

- **Skill Taxonomy**: Expanded keyword database
  - Programming languages: Python, Java, JavaScript, TypeScript, Rust, Go, C++, C#, PHP, Ruby
  - Frameworks: React, Vue, Angular, Django, Flask, FastAPI, Spring, Node.js
  - Databases: SQL, PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
  - Cloud/DevOps: Docker, Kubernetes, AWS, GCP, Azure, Jenkins, GitLab, Terraform
  - AI/ML: Machine Learning, Deep Learning, NLP, Computer Vision, TensorFlow, PyTorch
  - Soft skills (Vietnamese + English)

### 3. API Endpoints Updated
- **POST /ner/vi**: Now uses PhoBERT for Vietnamese skill extraction
  - Returns `model: "phobert"` when ML succeeds
  - Falls back to rules with `model: "fallback"` on errors
  - Extracts skills and years of experience
  
- **POST /score-cv**: Vietnamese scoring uses PhoBERT
  - Graceful fallback to rule-based on failure
  - English still uses rules (awaiting PR-5)

- **Startup preloading**: PhoBERT loads on service startup for faster first request

### 4. Testing Results ✅

**Vietnamese NER Test:**
Input:
```
Tôi có 5 năm kinh nghiệm với Python, React, Docker, PostgreSQL, AWS, Kubernetes.
```

Output:
```json
{
  "success": true,
  "data": {
    "language": "vi",
    "entities": [
      {"label": "SKILL", "text": "aws"},
      {"label": "SKILL", "text": "docker"},
      {"label": "SKILL", "text": "kubernetes"},
      {"label": "SKILL", "text": "postgresql"},
      {"label": "SKILL", "text": "python"},
      {"label": "SKILL", "text": "react"},
      {"label": "YEARS_EXPERIENCE", "text": "5"}
    ],
    "model": "phobert"
  }
}
```

**Vietnamese CV Scoring Test:**
CV: *"5 năm kinh nghiệm Python, React, Docker, PostgreSQL, AWS. Phát triển microservices và API RESTful."*

JD: *"Cần Senior Developer 3+ năm kinh nghiệm Python, Docker, AWS. Ưu tiên React và PostgreSQL."*

Result:
```json
{
  "score": 79.9,
  "strengths": [
    "Matched key skills: aws, docker, postgresql, python, react",
    "CV content aligns well with the target job description.",
    "Experience level meets requirement (5 years vs 3 years required)."
  ],
  "weaknesses": [
    "CV misses some standard sections (experience/skills/education/projects)."
  ],
  "improvement_tips": [
    "Add missing CV sections to improve recruiter readability and ATS matching."
  ]
}
```

## 📊 Performance & Model Info

- **Model Size**: ~400MB download (first run only)
- **Model**: `vinai/phobert-base` (135M parameters)
- **Inference Speed**: < 1 second for typical CV/JD pairs
- **Device**: Auto-detects CUDA if available, falls back to CPU
- **Caching**: Hugging Face cache at `C:\Users\<user>\.cache\huggingface\`

## 🔧 Technical Details

### Graceful Degradation
```python
# NLP service tries PhoBERT first
try:
    model = get_phobert()
    skills = model.extract_skills(text, "vi")
    return {"model": "phobert", "entities": [...]}
except Exception as e:
    logger.error(f"PhoBERT failed: {e}, using fallback")
    # Falls back to rule-based
    return {"model": "fallback", "entities": [...]}
```

### Backend Integration
Backend already configured from PR-3:
- Calls NLP service at `http://127.0.0.1:8001`
- Falls back to baseline if NLP unavailable
- No backend changes needed for PR-4

## 📝 Files Modified

1. **nlp-service/requirements.txt**: Added ML dependencies
2. **nlp-service/app/models.py**: Created (PhoBERT + BERT classes)
3. **nlp-service/app/main.py**: Updated NER endpoints + startup preloading
4. **nlp-service/README.md**: Updated documentation

## ⚠️ Known Issues & Warnings (Non-blocking)

1. **Symlink Warning**: Windows doesn't support symlinks by default in HuggingFace cache (degrades caching efficiency but still works)
2. **Deprecation Warning**: `resume_download` will be removed in huggingface_hub 1.0 (harmless)
3. **Xet Storage**: Optional optimization package not installed (minor performance impact)

## 🚀 Next Steps (PR-5)

- Implement English NER with BERT (`bert-base-uncased`)
- Unify skill extraction pipeline
- Add semantic similarity scoring (sentence-transformers)
- Performance benchmarking (PhoBERT vs BERT)

## ✅ Validation Checklist

- [x] ML dependencies installed
- [x] PhoBERT model loads successfully    
- [x] Vietnamese NER extracts skills correctly
- [x] Years of experience detected
- [x] CV scoring uses PhoBERT for Vietnamese
- [x] Graceful fallback works
- [x] Service starts without errors
- [x] Health endpoint responds
- [x] End-to-end integration tested
- [x] Documentation updated
