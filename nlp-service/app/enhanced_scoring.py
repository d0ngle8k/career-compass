"""
Enhanced CV Scoring with Related Skills Intelligence
Features:
- Related skills recognition (Vue.js ↔ React, MySQL ↔ PostgreSQL)
- Partial credit for skill category matches
- Field-specific weight adjustments
- Smarter baseline scoring
- Contextual soft skills detection from experience descriptions
"""
import re
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict
import math

# Import base class
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from advanced_scoring import AdvancedCVScorer


class EnhancedCVScorer(AdvancedCVScorer):
    """Enhanced scorer with related skills and smarter weighting"""
    
    # Related skills mapping - if CV has key, give partial credit for all values
    RELATED_SKILLS = {
        # Frontend frameworks
        "react": ["vue", "vue.js", "angular", "svelte"],
        "vue": ["react", "vue.js", "angular"],
        "vue.js": ["react", "vue", "angular"],
        "angular": ["react", "vue", "vue.js"],
        
        # Backend frameworks
        "express": ["fastapi", "flask", "django", "nest.js"],
        "fastapi": ["express", "flask", "django"],
        "django": ["fastapi", "flask", "rails"],
        "flask": ["fastapi", "django", "express"],
        "spring boot": ["spring", "nest.js", "express"],
        
        # Databases
        "postgresql": ["mysql", "mariadb", "postgres"],
        "mysql": ["postgresql", "mariadb"],
        "mongodb": ["dynamodb", "cassandra", "cosmosdb"],
        "redis": ["memcached", "elasticache"],
        
        # Cloud providers
        "aws": ["azure", "gcp", "google cloud"],
        "azure": ["aws", "gcp"],
        "gcp": ["aws", "azure", "google cloud"],
        "google cloud": ["gcp", "aws", "azure"],
        
        # Container orchestration
        "kubernetes": ["k8s", "docker swarm", "nomad"],
        "k8s": ["kubernetes", "docker swarm"],
        "docker": ["podman", "containerd"],
        
        # CI/CD
        "jenkins": ["github actions", "gitlab ci", "circleci"],
        "github actions": ["gitlab ci", "jenkins", "circleci"],
        "gitlab ci": ["github actions", "jenkins", "circleci"],
        
        # Programming languages
        "javascript": ["typescript"],
        "typescript": ["javascript"],
        "python": ["java", "go", "c#"],
        
        # Methodologies
        "agile": ["scrum", "kanban"],
        "scrum": ["agile", "kanban"],
        "rest": ["restful", "rest api", "graphql"],
        "restful": ["rest", "rest api"],
        "graphql": ["rest", "restful"],
    }
    
    # Soft skills that can be inferred from experience descriptions
    SOFT_SKILL_CONTEXTS = {
        "leadership": [
            r"\b(led|leading|lead)\s+(a\s+)?team",
            r"\bmanaged?\s+\d+\s+(?:people|developers|engineers|members)",
            r"\b(mentor|mentored|mentoring)",
            r"\b(supervised|supervising)",
        ],
        "teamwork": [
            r"\b(collaborated?|collaborating)\s+with",
            r"\b(worked?|working)\s+(?:with|in)\s+(?:a\s+)?team",
            r"\bcross-functional\s+team",
            r"\bteam\s+(?:player|member)",
        ],
        "communication": [
            r"\b(presented?|presenting)\s+(?:to|at)",
            r"\b(communicated?|communicating)\s+with",
            r"\bstakeholder\s+(?:management|communication)",
            r"\b(documented?|documenting)",
            r"\b(reported?|reporting)\s+to",
        ],
        "problem solving": [
            r"\b(solved?|solving|resolved?|resolving)\s+(?:complex\s+)?(?:problems?|issues?)",
            r"\b(debugged?|debugging)",
            r"\b(troubleshot|troubleshooting)",
            r"\b(optimized?|optimizing|improved?)",
        ],
        "analytical": [
            r"\b(analyzed?|analyzing|analysed?|analysing)",
            r"\b(evaluated?|evaluating)",
            r"\b(assessed?|assessing)",
            r"\bdata-driven",
        ],
        "project management": [
            r"\b(managed?|managing)\s+(?:projects?|initiatives?)",
            r"\b(coordinated?|coordinating)",
            r"\b(planned?|planning)\s+and\s+(?:executed?|implementing)",
            r"\bproject\s+manager",
        ],
    }
    
    # Field-specific scoring weights
    FIELD_WEIGHTS = {
        "software": {
            "technical_skills": 0.45,
            "soft_skills": 0.10,
            "methodologies": 0.10,
            "experience": 0.20,
            "education": 0.08,
            "certifications": 0.02,
            "structure": 0.05
        },
        "data": {
            "technical_skills": 0.45,
            "soft_skills": 0.10,
            "methodologies": 0.10,
            "experience": 0.20,
            "education": 0.10,
            "certifications": 0.02,
            "structure": 0.03
        },
        "marketing": {
            "technical_skills": 0.25,
            "soft_skills": 0.25,
            "methodologies": 0.10,
            "experience": 0.25,
            "education": 0.08,
            "certifications": 0.02,
            "structure": 0.05
        },
        "finance": {
            "technical_skills": 0.20,
            "soft_skills": 0.20,
            "methodologies": 0.10,
            "experience": 0.25,
            "education": 0.10,
            "certifications": 0.10,
            "structure": 0.05
        },
        "hr": {
            "technical_skills": 0.15,
            "soft_skills": 0.30,
            "methodologies": 0.10,
            "experience": 0.25,
            "education": 0.10,
            "certifications": 0.05,
            "structure": 0.05
        },
        "default": {
            "technical_skills": 0.40,
            "soft_skills": 0.15,
            "methodologies": 0.05,
            "experience": 0.20,
            "education": 0.10,
            "certifications": 0.05,
            "structure": 0.05
        }
    }
    
    def infer_soft_skills_from_context(self, text: str) -> Set[str]:
        """Detect soft skills from experience descriptions"""
        inferred = set()
        text_lower = text.lower()
        
        for skill, patterns in self.SOFT_SKILL_CONTEXTS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    inferred.add(skill)
                    break  # Found this skill, move to next
        
        return inferred
    
    def calculate_related_skill_matches(
        self,
        cv_skills: Set[str],
        jd_skills: Set[str]
    ) -> Dict[str, float]:
        """
        Calculate skill matches with partial credit for related skills
        Returns: dict with skill -> match_score (1.0 for exact, 0.5 for related)
        """
        matches = {}
        
        for jd_skill in jd_skills:
            # Exact match
            if jd_skill in cv_skills:
                matches[jd_skill] = 1.0
            # Check related skills
            elif jd_skill in self.RELATED_SKILLS:
                related = self.RELATED_SKILLS[jd_skill]
                for cv_skill in cv_skills:
                    if cv_skill in related:
                        # Give 60% credit for related skill
                        matches[jd_skill] = max(matches.get(jd_skill, 0), 0.6)
        
        return matches
    
    def detect_field_from_jd(self, jd_text: str) -> str:
        """Detect job field from JD content"""
        jd_lower = jd_text.lower()
        
        # Software/Engineering indicators
        if any(keyword in jd_lower for keyword in [
            "software engineer", "backend developer", "frontend developer",
            "full stack", "devops", "system architect", "programmer"
        ]):
            return "software"
        
        # Data/AI indicators
        if any(keyword in jd_lower for keyword in [
            "data scientist", "data engineer", "machine learning",
            "data analyst", "business intelligence", "ai engineer"
        ]):
            return "data"
        
        # Marketing indicators
        if any(keyword in jd_lower for keyword in [
            "marketing manager", "digital marketing", "content marketing",
            "social media", "brand manager", "marketing specialist"
        ]):
            return "marketing"
        
        # Finance indicators
        if any(keyword in jd_lower for keyword in [
            "financial analyst", "accountant", "finance manager",
            "investment", "auditor", "controller", "treasury"
        ]):
            return "finance"
        
        # HR indicators
        if any(keyword in jd_lower for keyword in [
            "human resources", "talent acquisition", "recruiter",
            "hr manager", "people operations", "hr specialist"
        ]):
            return "hr"
        
        return "default"
    
    def score_cv(self, cv_text: str, jd_text: str, language: str = "vi") -> Dict:
        """
        Enhanced CV scoring with related skills and field-specific weights
        """
        
        # Detect field to use appropriate weights
        field = self.detect_field_from_jd(jd_text)
        weights = self.FIELD_WEIGHTS.get(field, self.FIELD_WEIGHTS["default"])
        
        # Extract keywords from both texts
        cv_tech = self.extract_keywords(cv_text, "technical")
        jd_tech = self.extract_keywords(jd_text, "technical")
        
        # Get soft skills - both explicit and inferred
        cv_soft_explicit = self.extract_keywords(cv_text, "soft")
        cv_soft_inferred = self.infer_soft_skills_from_context(cv_text)
        cv_soft = cv_soft_explicit | cv_soft_inferred
        
        jd_soft = self.extract_keywords(jd_text, "soft")
        
        cv_method = self.extract_keywords(cv_text, "methodology")
        jd_method = self.extract_keywords(jd_text, "methodology")
        
        # Calculate matches with related skills credit
        tech_matches = self.calculate_related_skill_matches(cv_tech, jd_tech)
        matched_tech = set(tech_matches.keys())
        missing_tech = jd_tech - matched_tech
        
        # Soft skills - simple matching (with inferred skills)
        matched_soft = cv_soft & jd_soft
        missing_soft = jd_soft - cv_soft
        
        # Methodologies - related matching
        method_matches = self.calculate_related_skill_matches(cv_method, jd_method)
        matched_method = set(method_matches.keys())
        missing_method = jd_method - matched_method
        
        # Get keyword importance weights
        jd_tech_weights = self.calculate_keyword_importance(jd_tech)
        
        # Calculate weighted technical skills score with related skills credit
        if jd_tech:
            total_tech_weight = sum(jd_tech_weights.values())
            matched_tech_weight = sum(
                jd_tech_weights.get(k, 1.0) * tech_matches[k]  # Multiply by match quality
                for k in matched_tech
            )
            tech_score = (matched_tech_weight / total_tech_weight) * 100
            # Add small bonus for having extra relevant skills
            extra_skills = cv_tech - jd_tech
            if extra_skills:
                bonus = min(10, len(extra_skills) * 2)
                tech_score = min(100, tech_score + bonus)
        else:
            tech_score = 60  # Default if no technical skills in JD
        
        # Calculate soft skills score
        if jd_soft:
            soft_score = (len(matched_soft) / len(jd_soft)) * 100
            # Bonus for having more soft skills than required
            if len(matched_soft) > len(jd_soft) * 0.7:
                soft_score = min(100, soft_score + 10)
        else:
            soft_score = 60 if cv_soft else 50
        
        # Calculate methodology score with related skills
        if jd_method:
            total_method_match = sum(method_matches.values())
            method_score = (total_method_match / len(jd_method)) * 100
        else:
            method_score = 60
        
        # Experience matching (same as before)
        cv_years = self.extract_years_experience(cv_text)
        jd_years = self.extract_years_experience(jd_text)
        
        if jd_years > 0:
            if cv_years >= jd_years:
                exp_score = min(100, 90 + (cv_years - jd_years) * 2)
            elif cv_years >= jd_years - 1:
                exp_score = 80
            elif cv_years >= jd_years - 2:
                exp_score = 65
            elif cv_years >= max(1, jd_years - 3):
                exp_score = 50
            else:
                exp_score = max(35, 50 - (jd_years - cv_years) * 5)
        else:
            exp_score = 65 if cv_years > 2 else 50
        
        # Education matching
        cv_edu = self.detect_education_level(cv_text)
        jd_edu = self.detect_education_level(jd_text)
        edu_score = self._calculate_education_score(cv_edu, jd_edu)
        
        # Certifications & achievements
        cv_certs = self.detect_certifications(cv_text)
        jd_certs = self.detect_certifications(jd_text)
        
        if jd_certs:
            matched_certs = set(cv_certs) & set(jd_certs)
            cert_score = (len(matched_certs) / len(jd_certs)) * 100
        else:
            cert_score = 60 if cv_certs else 50
        
        # CV structure quality
        sections = self.detect_cv_sections(cv_text)
        structure_score = (sum(sections.values()) / len(sections)) * 100
        
        # Calculate final weighted score using field-specific weights
        final_score = (
            tech_score * weights["technical_skills"] +
            soft_score * weights["soft_skills"] +
            method_score * weights["methodologies"] +
            exp_score * weights["experience"] +
            edu_score * weights["education"] +
            cert_score * weights["certifications"] +
            structure_score * weights["structure"]
        )
        
        # Apply baseline floor - any complete CV gets at least 35
        if structure_score >= 60:  # Has most standard sections
            final_score = max(40, final_score)
        
        # Generate detailed feedback
        feedback = self._generate_enhanced_feedback(
            matched_tech, missing_tech, tech_matches,
            matched_soft, missing_soft, cv_soft_inferred,
            matched_method, missing_method,
            cv_years, jd_years,
            cv_edu, jd_edu,
            cv_certs, jd_certs,
            sections,
            field,
            language
        )
        
        return {
            "score": round(final_score, 2),
            "breakdown": {
                "technical_skills": round(tech_score, 2),
                "soft_skills": round(soft_score, 2),
                "methodologies": round(method_score, 2),
                "experience": round(exp_score, 2),
                "education": round(edu_score, 2),
                "certifications": round(cert_score, 2),
                "structure": round(structure_score, 2)
            },
            "strengths": feedback["strengths"],
            "weaknesses": feedback["weaknesses"],
            "improvement_tips": feedback["tips"],
            "matched_keywords": {
                "technical": sorted(list(matched_tech)),
                "soft_skills": sorted(list(matched_soft)),
                "methodologies": sorted(list(matched_method))
            },
            "missing_keywords": {
                "technical": sorted(list(missing_tech)),
                "soft_skills": sorted(list(missing_soft)),
                "methodologies": sorted(list(missing_method))
            },
            "metadata": {
                "cv_years": cv_years,
                "jd_years": jd_years,
                "cv_education": cv_edu,
                "jd_education": jd_edu,
                "cv_certifications": cv_certs,
                "jd_certifications": jd_certs,
                "cv_sections": sections,
                "detected_field": field,
                "inferred_soft_skills": sorted(list(cv_soft_inferred)),
                "related_skill_matches": {k: v for k, v in tech_matches.items() if v < 1.0}
            }
        }
    
    def _generate_enhanced_feedback(
        self,
        matched_tech, missing_tech, tech_matches,
        matched_soft, missing_soft, inferred_soft,
        matched_method, missing_method,
        cv_years, jd_years,
        cv_edu, jd_edu,
        cv_certs, jd_certs,
        sections,
        field,
        language
    ) -> Dict[str, List[str]]:
        """Generate enhanced feedback with related skills information"""
        
        # Use parent class feedback generation as base
        base_feedback = self._generate_feedback(
            matched_tech, missing_tech,
            matched_soft, missing_soft,
            matched_method, missing_method,
            cv_years, jd_years,
            cv_edu, jd_edu,
            cv_certs, jd_certs,
            sections,
            language
        )
        
        strengths = base_feedback["strengths"]
        weaknesses = base_feedback["weaknesses"]
        tips = base_feedback["tips"]
        
        # Add related skills information
        related_matches = {k: v for k, v in tech_matches.items() if v < 1.0}
        if related_matches:
            related_list = ",".join(list(related_matches.keys())[:3])
            strengths.insert(0, f"✓ Related experience with: {related_list} (partial match)")
        
        # Add inferred soft skills information
        if inferred_soft:
            strengths.append(f"✓ Demonstrated soft skills: {', '.join(sorted(list(inferred_soft))[:5])}")
        
        # Add field-specific tips
        if field == "software" and missing_tech:
            tips.append(f"→ Focus on core software skills: {', '.join(list(missing_tech)[:3])}")
        elif field in ["marketing", "hr"] and missing_soft:
            tips.append(f"→ Highlight interpersonal skills: {', '.join(list(missing_soft)[:3])}")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "tips": tips
        }


# Create singleton instance
_enhanced_scorer_instance = None

def get_enhanced_scorer() -> EnhancedCVScorer:
    """Get singleton instance of enhanced scorer"""
    global _enhanced_scorer_instance
    if _enhanced_scorer_instance is None:
        _enhanced_scorer_instance = EnhancedCVScorer()
    return _enhanced_scorer_instance
