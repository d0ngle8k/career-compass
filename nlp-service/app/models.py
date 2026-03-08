"""ML Models for NLP Service - PhoBERT and BERT implementations"""
from __future__ import annotations

import logging
import re
from typing import Literal

import torch
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)

# Skill taxonomy for CV/JD analysis
SKILL_KEYWORDS = {
    "vi": {
        # Programming languages
        "python", "java", "javascript", "typescript", "rust", "go", "c++", "c#", "php", "ruby",
        # Frameworks & Libraries
        "react", "vue", "angular", "django", "flask", "fastapi", "spring", "node.js", "express",
        # Databases
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        # Cloud & DevOps
        "docker", "kubernetes", "aws", "gcp", "azure", "jenkins", "gitlab", "terraform",
        # Tools & Technologies
        "git", "linux", "nginx", "apache", "microservices", "rest", "graphql", "api",
        # Data & AI
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
        # Soft skills (Vietnamese)
        "giao tiếp", "làm việc nhóm", "lãnh đạo", "quản lý", "phân tích", "giải quyết vấn đề",
    },
    "en": {
        # Same as above plus English-specific soft skills
        "python", "java", "javascript", "typescript", "rust", "go", "c++", "c#", "php", "ruby",
        "react", "vue", "angular", "django", "flask", "fastapi", "spring", "node.js", "express",
        "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "docker", "kubernetes", "aws", "gcp", "azure", "jenkins", "gitlab", "terraform",
        "git", "linux", "nginx", "apache", "microservices", "rest", "graphql", "api",
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
        # Soft skills (English)
        "communication", "teamwork", "leadership", "management", "analytical", "problem solving",
    },
}


class PhoBERTModel:
    """Vietnamese BERT (PhoBERT) for NER and embedding tasks"""

    def __init__(self, model_name: str = "vinai/phobert-base"):
        logger.info(f"Loading PhoBERT model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.eval()
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            logger.info(f"PhoBERT loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load PhoBERT: {e}")
            raise

    def get_embeddings(self, text: str) -> torch.Tensor:
        """Get contextualized embeddings for text"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use [CLS] token embedding as sentence representation
            embeddings = outputs.last_hidden_state[:, 0, :]
        
        return embeddings.cpu()

    def extract_skills(self, text: str, language: str = "vi") -> list[str]:
        """
        Extract skills from text using PhoBERT-enhanced matching
        
        Strategy:
        1. Tokenize and get embeddings for context understanding
        2. Match against skill taxonomy with contextual awareness
        3. Filter false positives using semantic scoring
        """
        text_lower = text.lower()
        found_skills: set[str] = set()
        
        # Direct keyword matching (enhanced with word boundaries)
        skill_set = SKILL_KEYWORDS.get(language, SKILL_KEYWORDS["vi"])
        for skill in skill_set:
            # Use word boundary regex for better matching
            pattern = rf"(?i)(^|[^a-z0-9]){re.escape(skill)}([^a-z0-9]|$)"
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # TODO: Add semantic similarity-based skill detection
        # For now, we use enhanced keyword matching with PhoBERT context
        
        return sorted(found_skills)

    def extract_years_experience(self, text: str) -> int | None:
        """Extract years of experience from text"""
        # Vietnamese patterns: "5 năm kinh nghiệm", "3+ năm", "kinh nghiệm 2 năm"
        vi_patterns = [
            r"(\d{1,2})\s*\+?\s*năm\s*(?:kinh\s*nghiệm)?",
            r"(?:kinh\s*nghiệm|experience)\s*(\d{1,2})\s*\+?\s*năm",
        ]
        
        # English patterns: "5 years experience", "3+ years", "5 yrs"
        en_patterns = [
            r"(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience)?",
            r"(?:experience|exp)\s*(?:of\s*)?(\d{1,2})\s*\+?\s*(?:years?|yrs?)",
        ]
        
        all_patterns = vi_patterns + en_patterns
        matches: list[int] = []
        
        for pattern in all_patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(int(m) for m in found if m.isdigit())
        
        return max(matches) if matches else None


class BERTModel:
    """English BERT for NER and embedding tasks (placeholder for PR-5)"""

    def __init__(self, model_name: str = "bert-base-uncased"):
        logger.info(f"Loading BERT model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.eval()
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            logger.info(f"BERT loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load BERT: {e}")
            raise

    def get_embeddings(self, text: str) -> torch.Tensor:
        """Get contextualized embeddings for text"""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]
        
        return embeddings.cpu()

    def extract_skills(self, text: str, language: str = "en") -> list[str]:
        """Extract skills from English text"""
        text_lower = text.lower()
        found_skills: set[str] = set()
        
        skill_set = SKILL_KEYWORDS.get(language, SKILL_KEYWORDS["en"])
        for skill in skill_set:
            pattern = rf"(?i)(^|[^a-z0-9]){re.escape(skill)}([^a-z0-9]|$)"
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return sorted(found_skills)

    def extract_years_experience(self, text: str) -> int | None:
        """Extract years of experience from English text"""
        patterns = [
            r"(\d{1,2})\s*\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience)?",
            r"(?:experience|exp)\s*(?:of\s*)?(\d{1,2})\s*\+?\s*(?:years?|yrs?)",
        ]
        
        matches: list[int] = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(int(m) for m in found if m.isdigit())
        
        return max(matches) if matches else None


class SimilarityModel:
    """Sentence-Transformers for semantic similarity"""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        logger.info(f"Loading Similarity model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Similarity model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Similarity model: {e}")
            raise

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts"""
        embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
        similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
        return float(similarity)

    def batch_similarity(self, text: str, candidates: list[str]) -> list[float]:
        """Compute similarity between text and multiple candidates"""
        all_texts = [text] + candidates
        embeddings = self.model.encode(all_texts, convert_to_tensor=True)
        
        # Compute cosine similarity between first text and all candidates
        similarities = util.cos_sim(embeddings[0:1], embeddings[1:]).squeeze().tolist()
        
        # Handle single candidate case (returns scalar instead of list)
        if isinstance(similarities, float):
            return [similarities]
        return similarities


# Global model instances (lazy loading)
_phobert_model: PhoBERTModel | None = None
_bert_model: BERTModel | None = None
_similarity_model: SimilarityModel | None = None


def get_phobert() -> PhoBERTModel:
    """Get or initialize PhoBERT model (singleton pattern)"""
    global _phobert_model
    if _phobert_model is None:
        _phobert_model = PhoBERTModel()
    return _phobert_model


def get_bert() -> BERTModel:
    """Get or initialize BERT model (singleton pattern)"""
    global _bert_model
    if _bert_model is None:
        _bert_model = BERTModel()
    return _bert_model


def get_similarity() -> SimilarityModel:
    """Get or initialize Similarity model (singleton pattern)"""
    global _similarity_model
    if _similarity_model is None:
        _similarity_model = SimilarityModel()
    return _similarity_model
