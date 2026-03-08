# NLP Service (PR-4: PhoBERT Integration)

Production NLP service with PhoBERT for Vietnamese CV/JD analysis.

## Features

- **PhoBERT-powered Vietnamese NER**: Real transformer-based skill extraction and entity recognition
- **Graceful fallback**: Automatically falls back to rule-based analysis if ML models fail
- **Lazy loading**: Models loaded on first use to reduce startup time
- **FastAPI**: High-performance async API

## Requirements

- Python 3.11+
- PyTorch 2.1+
- Transformers (Hugging Face)
- FastAPI + Uvicorn

## Run local

```bash
cd nlp-service

# Use Python 3.11 virtual environment
py -3.11 -m venv .venv311
.venv311\Scripts\activate

# Install dependencies (includes torch, transformers)
pip install -r requirements.txt

# Start service
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

**Note**: First startup downloads PhoBERT model (~400MB) from Hugging Face. Subsequent starts are faster.

## Endpoints

- `GET /health` - Health check
- `POST /score-cv` - Score CV against JD (uses PhoBERT for Vietnamese)
- `POST /ner/vi` - Vietnamese NER with PhoBERT
- `POST /ner/en` - English NER (rule-based for now, BERT in PR-5)
- `POST /similarity` - Text similarity

## Implementation Details

### PR-4: PhoBERT for Vietnamese
- Model: `vinai/phobert-base` (135M parameters)
- Skills: Enhanced keyword matching with contextual embeddings
- Years extraction: Multi-pattern regex with Vietnamese language support
- Fallback: Graceful degradation to rule-based if model fails

### Future: PR-5 BERT for English
- Will add `bert-base-uncased` for English NER
- Unified skill extraction pipeline
