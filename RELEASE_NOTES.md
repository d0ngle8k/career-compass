# Release Notes - Career Compass AI v0.2.0

## Overview
This release represents a major upgrade to the Career Compass AI platform, focusing on enhancing the NLP capabilities with state-of-the-art transformer models and introducing a template-based content generation system.

## 🚀 New Features

### PR-4: PhoBERT Vietnamese NER Integration
- **Vietnamese Language Support**: Integrated PhoBERT (vinai/phobert-base) for accurate Vietnamese skill extraction
- **Named Entity Recognition**: Automatically extracts skills and years of experience from Vietnamese CVs
- **Fallback System**: Graceful degradation to rule-based extraction if model fails

### PR-5: BERT English NER + Semantic Similarity
- **English Language Support**: Activated BERT (bert-base-uncased) for English skill extraction
- **Semantic Similarity**: Implemented sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2) for computing text similarity
- **Unified Pipeline**: Both Vietnamese and English now use transformer-based models
- **Dependencies Added**:
  - `sentence-transformers==2.7.0`
  - `scikit-learn==1.3.2`

### PR-6: Template Engine for Email & Cover Letters
- **Template-Based Generation**: Replaced AI-generated content with professional Tera templates
- **Multi-Language Support**: Templates for both Vietnamese (`vi`) and English (`en`)
- **Style Variations**: Formal and casual styles for all content types
- **Content Types**:
  - Email subjects
  - Email bodies
  - Cover letters
- **Smart Context Extraction**: Automatically extracts candidate name, skills, years of experience, company name, and position from CV/JD

### PR-7: Gemini Chat-Only Refactor
- **Focused AI Usage**: Gemini API now exclusively handles chat assistant functionality
- **Code Cleanup**: Removed unused JSON generation functions
- **Improved Maintainability**: Clearer separation of concerns between template-based and AI-driven content

## 🔧 Technical Improvements

### NLP Service (v0.2.0)
- **Three ML Models**: PhoBERT, BERT, and Sentence-Transformers loaded at startup
- **Model Preloading**: All models cached in memory for fast inference
- **Graceful Fallback**: Rule-based extraction when models unavailable
- **Model Attribution**: API responses indicate which model was used (`phobert`, `bert`, `sentence-transformers`, or `fallback`)

### Backend Service
- **New Dependency**: `tera = "1.20"` for template rendering
- **Template Initialization**: Templates loaded at application startup
- **Zero Warnings**: Clean compilation with no dead code warnings

## 📊 API Changes

### NLP Service Endpoints

#### `/score-cv` (Enhanced)
- Now uses BERT for English and PhoBERT for Vietnamese
- Returns model used in response metadata

#### `/ner/en` (Enhanced)
- Uses BERT instead of fallback-only approach
- Returns `model: "bert"` in successful responses

#### `/ner/vi` (Enhanced)
- Uses PhoBERT for Vietnamese text
- Returns `model: "phobert"` in responses

#### `/similarity` (New Endpoint)
- Computes semantic similarity between two texts
- Uses sentence-transformers with cosine similarity
- Returns similarity score (0.0 to 1.0)
- Fallback to Jaccard similarity if model fails

### Backend Endpoints

#### `/api/v1/content/generate-email` (Behavior Change)
- Now uses templates instead of Gemini
- Faster response times
- Consistent formatting
- Supports `language` ("vi" | "en") and `template_style` ("formal" | "casual")

#### `/api/v1/content/generate-cover-letter` (Behavior Change)
- Uses templates for generation
- Professional formatting
- Parameters: `cv_text`, `jd_text`, `language`, `template_style`

## 🧪 Testing & QA

### New Test Suite
- Comprehensive endpoint testing (`tests/test_endpoints.py`)
- Performance benchmarks
- Language-specific test cases
- Model validation tests

### Test Coverage
- Health endpoint validation
- CV scoring (English & Vietnamese)
- NER (English & Vietnamese)
- Semantic similarity (similar & dissimilar texts)
- Performance benchmarks (< 3s response time)

## 📝 Documentation Updates

### README Enhancements
- Updated architecture diagrams
- NLP model documentation
- Template system guide
- API endpoint examples
- Setup instructions for new dependencies

## 🔄 Migration Guide

### For Developers

1. **NLP Service Dependencies**:
   ```bash
   cd nlp-service
   pip install sentence-transformers==2.7.0 scikit-learn==1.3.2
   ```

2. **Backend Dependencies**:
   ```bash
   cd backend
   cargo build
   ```

3. **First Run**: Models will download automatically (~900MB total):
   - PhoBERT: ~400MB
   - BERT: ~440MB
   - Sentence-Transformers: ~470MB

4. **Templates**: Ensure `backend/templates/` directory exists with all `.tera` files

### For API Consumers

- **No Breaking Changes**: Email and cover letter endpoints maintain same interface
- **Response Times**: Expect faster responses (templates vs AI generation)
- **Content Quality**: More consistent formatting, professional tone

## ⚠️ Known Issues

- **Windows Build**: Linker may encounter file locking issues in some environments
  - Workaround: Use `cargo check` or run `cargo clean` before building
- **First Run**: Initial model downloads may take 2-3 minutes depending on connection speed

## 📦 Dependencies

### Python (NLP Service)
- fastapi==0.108.0
- uvicorn[standard]==0.25.0
- pydantic==2.5.3
- torch==2.1.1
- transformers==4.35.2
- sentencepiece==0.1.99
- numpy<2
- sentence-transformers==2.7.0 **(new)**
- scikit-learn==1.3.2 **(new)**

### Rust (Backend)
- tera = "1.20" **(new)**
- axum = "0.7"
- tokio = "1"
- serde = "1"
- serde_json = "1"
- (see Cargo.toml for complete list)

## 🎯 Performance Metrics

- **NER Latency**: < 3 seconds per request (including model inference)
- **Template Rendering**: < 50ms per template
- **Model Loading**: 20-40 seconds on startup (3 models)
- **Memory Usage**: ~2.5GB (with all models loaded)

## 🙏 Credits

- **PhoBERT**: VinAI Research
- **BERT**: Google Research
- **Sentence-Transformers**: UKPLab
- **Tera**: Community-driven template engine

## 📅 Release Date
March 2026

---

For detailed technical documentation, see the project README.md and individual module documentation.
