from __future__ import annotations

import logging
import re
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.models import get_bert, get_phobert, get_similarity
from app.improved_scoring import improved_score_cv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Career Compass NLP Service", version="0.2.0")


@app.on_event("startup")
async def startup_event():
    """Preload models on startup for faster first request"""
    logger.info("Preloading ML models...")
    try:
        # Preload PhoBERT for Vietnamese
        get_phobert()
        logger.info("PhoBERT loaded successfully")
    except Exception as e:
        logger.warning(f"Could not preload PhoBERT: {e}. Will use fallback.")
    
    try:
        # Preload BERT for English
        get_bert()
        logger.info("BERT loaded successfully")
    except Exception as e:
        logger.warning(f"Could not preload BERT: {e}. Will use fallback.")
    
    try:
        # Preload Similarity model
        get_similarity()
        logger.info("Similarity model loaded successfully")
    except Exception as e:
        logger.warning(f"Could not preload Similarity: {e}. Will use fallback.")
    
    logger.info("NLP service ready")


class ScoreCvRequest(BaseModel):
    cv_text: str = Field(min_length=1)
    jd_text: str = Field(min_length=1)
    language: Literal["vi", "en"] | str = "vi"


class ScoreCvResponse(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    improvement_tips: list[str]


class Envelope(BaseModel):
    success: bool
    data: ScoreCvResponse | dict | None = None
    error: str | None = None


class NerRequest(BaseModel):
    text: str


class SimilarityRequest(BaseModel):
    left_text: str
    right_text: str


def _extract_years(text: str) -> int | None:
    matches = re.findall(r"(?i)\b(\d{1,2})\s*\+?\s*(years?|yrs?|n[aă]m)\b", text)
    if not matches:
        return None
    return max(int(m[0]) for m in matches)


def _skills() -> list[str]:
    return [
        "rust",
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node",
        "sql",
        "postgresql",
        "docker",
        "kubernetes",
        "aws",
        "gcp",
        "azure",
        "git",
    ]


def _skill_hits(text: str) -> set[str]:
    lower = text.lower()
    found: set[str] = set()
    for skill in _skills():
        pattern = rf"(?i)(^|[^a-z0-9]){re.escape(skill)}([^a-z0-9]|$)"
        if re.search(pattern, lower):
            found.add(skill)
    return found


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-zA-Z0-9+#]+", text.lower())
        if len(token.strip()) >= 2
    }


def _score(cv_text: str, jd_text: str, language: str) -> ScoreCvResponse:
    # Use PhoBERT for Vietnamese, BERT for English
    try:
        if language.lower() == "vi":
            model = get_phobert()
            cv_skills = set(model.extract_skills(cv_text, "vi"))
            jd_skills = set(model.extract_skills(jd_text, "vi"))
        else:
            model = get_bert()
            cv_skills = set(model.extract_skills(cv_text, "en"))
            jd_skills = set(model.extract_skills(jd_text, "en"))
    except Exception as e:
        logger.warning(f"ML model failed, using fallback: {e}")
        cv_skills = _skill_hits(cv_text)
        jd_skills = _skill_hits(jd_text)

    matched = sorted(cv_skills & jd_skills)
    missing = sorted(jd_skills - cv_skills)

    must_have = (len(matched) / len(jd_skills)) if jd_skills else 0.7

    cv_tokens = _tokenize(cv_text)
    jd_tokens = _tokenize(jd_text)
    overlap = (len(cv_tokens & jd_tokens) / len(cv_tokens | jd_tokens)) if (cv_tokens and jd_tokens) else 0.0

    cv_years = _extract_years(cv_text)
    jd_years = _extract_years(jd_text)
    if cv_years is not None and jd_years is not None and jd_years > 0:
        exp_fit = min(cv_years / jd_years, 1.0)
    elif cv_years is not None:
        exp_fit = 0.7
    elif jd_years is not None:
        exp_fit = 0.3
    else:
        exp_fit = 0.6

    lower = cv_text.lower()
    sections = ["experience", "skills", "education", "project"]
    if str(language).lower() == "vi":
        sections = ["kinh nghiệm", "kỹ năng", "học vấn", "dự án"]
    section_score = sum(1 for section in sections if section in lower) / len(sections)

    score = 100.0 * (0.50 * must_have + 0.20 * overlap + 0.20 * exp_fit + 0.10 * section_score)
    if len(missing) >= 3:
        score -= 12.0
    elif missing:
        score -= 5.0
    score = round(max(0.0, min(100.0, score)), 1)

    strengths: list[str] = []
    weaknesses: list[str] = []
    tips: list[str] = []

    if matched:
        strengths.append(f"Matched key skills: {', '.join(matched)}")
    if overlap >= 0.35:
        strengths.append("CV content aligns well with the target job description.")

    if cv_years is not None and jd_years is not None and cv_years >= jd_years:
        strengths.append(f"Experience level meets requirement ({cv_years} years vs {jd_years} years required).")

    if missing:
        weaknesses.append(f"Missing or unclear required skills: {', '.join(missing)}")
        tips.append("Add concrete evidence for missing skills via projects or quantified achievements.")

    if section_score < 0.75:
        weaknesses.append("CV misses some standard sections (experience/skills/education/projects).")
        tips.append("Add missing CV sections to improve recruiter readability and ATS matching.")

    if not strengths:
        strengths.append("CV contains relevant signals but needs clearer alignment with JD.")
    if not weaknesses:
        weaknesses.append("No major gaps detected from baseline rule-based analysis.")
    if not tips:
        tips.append("Tailor summary and bullet points directly to JD keywords and outcomes.")

    return ScoreCvResponse(
        score=score,
        strengths=strengths,
        weaknesses=weaknesses,
        improvement_tips=tips,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/score-cv", response_model=Envelope)
def score_cv(payload: ScoreCvRequest) -> Envelope:
    try:
        result_dict = improved_score_cv(payload.cv_text, payload.jd_text, payload.language)
        result = ScoreCvResponse(
            score=result_dict["score"],
            strengths=result_dict["strengths"],
            weaknesses=result_dict["weaknesses"],
            improvement_tips=result_dict["improvement_tips"]
        )
        return Envelope(success=True, data=result)
    except Exception as e:
        logger.error(f"Scoring error: {e}")
        # Fallback to original scoring
        result = _score(payload.cv_text, payload.jd_text, payload.language)
        return Envelope(success=True, data=result)


@app.post("/ner/vi")
def ner_vi(payload: NerRequest) -> dict:
    """Vietnamese NER using PhoBERT"""
    try:
        model = get_phobert()
        skills = model.extract_skills(payload.text, "vi")
        years = model.extract_years_experience(payload.text)
        
        entities = [{"label": "SKILL", "text": skill} for skill in skills]
        if years is not None:
            entities.append({"label": "YEARS_EXPERIENCE", "text": str(years)})
        
        return {"success": True, "data": {"language": "vi", "entities": entities, "model": "phobert"}}
    except Exception as e:
        logger.error(f"PhoBERT NER failed: {e}, using fallback")
        # Fallback to rule-based
        years = _extract_years(payload.text)
        skills = sorted(_skill_hits(payload.text))
        entities = [{"label": "SKILL", "text": skill} for skill in skills]
        if years is not None:
            entities.append({"label": "YEARS_EXPERIENCE", "text": str(years)})
        return {"success": True, "data": {"language": "vi", "entities": entities, "model": "fallback"}}


@app.post("/ner/en")
def ner_en(payload: NerRequest) -> dict:
    """English NER using BERT"""
    try:
        model = get_bert()
        skills = model.extract_skills(payload.text, "en")
        years = model.extract_years_experience(payload.text)
        
        entities = [{"label": "SKILL", "text": skill} for skill in skills]
        if years is not None:
            entities.append({"label": "YEARS_EXPERIENCE", "text": str(years)})
        
        return {"success": True, "data": {"language": "en", "entities": entities, "model": "bert"}}
    except Exception as e:
        logger.error(f"BERT NER failed: {e}, using fallback")
        # Fallback to rule-based
        years = _extract_years(payload.text)
        skills = sorted(_skill_hits(payload.text))
        entities = [{"label": "SKILL", "text": skill} for skill in skills]
        if years is not None:
            entities.append({"label": "YEARS_EXPERIENCE", "text": str(years)})
        return {"success": True, "data": {"language": "en", "entities": entities, "model": "fallback"}}


@app.post("/similarity")
def similarity(payload: SimilarityRequest) -> dict:
    """Semantic similarity using sentence-transformers"""
    try:
        model = get_similarity()
        score = model.compute_similarity(payload.left_text, payload.right_text)
        return {"success": True, "data": {"score": round(score, 4), "model": "sentence-transformers"}}
    except Exception as e:
        logger.error(f"Similarity model failed: {e}, using fallback")
        # Fallback to Jaccard similarity
        left = _tokenize(payload.left_text)
        right = _tokenize(payload.right_text)
        score = (len(left & right) / len(left | right)) if (left and right) else 0.0
        return {"success": True, "data": {"score": round(score, 4), "model": "jaccard"}}
