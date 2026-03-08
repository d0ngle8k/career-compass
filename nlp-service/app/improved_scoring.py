"""
Improved CV Scoring Algorithm with better matching logic
"""
import re
from typing import List, Dict, Tuple
from collections import Counter

def normalize_skill(skill: str) -> str:
    """Normalize skill name for better matching"""
    skill = skill.lower().strip()
    
    # Common variations mapping
    variations = {
        "js": "javascript",
        "ts": "typescript",
        "py": "python",
        "nodejs": "node.js",
        "node": "node.js",
        "reactjs": "react",
        "vuejs": "vue.js",
        "postgresql": "postgres",
        "mysql": "sql",
        "mongodb": "mongo",
        "k8s": "kubernetes",
        "ml": "machine learning",
        "ai": "artificial intelligence",
        "nlp": "natural language processing",
        "seo/sem": "seo",
        "c++": "cpp",
        "c#": "csharp",
        ".net": "dotnet"
    }
    
    return variations.get(skill, skill)

def extract_skills_advanced(text: str) -> List[str]:
    """Extract skills from text with better logic"""
    text = text.lower()
    
    # Comprehensive skill list (expanded)
    all_skills = [
        # Programming languages
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", 
        "php", "ruby", "swift", "kotlin", "scala", "r", "matlab", "julia",
        
        # Frontend
        "react", "vue.js", "vue", "angular", "svelte", "next.js", "nuxt.js",
        "html", "css", "sass", "less", "tailwind", "bootstrap", "jquery",
        
        # Backend
        "node.js", "express", "fastapi", "django", "flask", "spring boot", 
        "spring", ".net", "asp.net", "laravel", "rails", "gin",
        
        # Databases
        "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "cassandra",
        "oracle", "sqlite", "dynamodb", "elasticsearch", "neo4j",
        
        # Cloud & DevOps
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
        "terraform", "ansible", "jenkins", "gitlab", "github actions", "circleci",
        "prometheus", "grafana", "elk", "nginx", "apache",
        
        # Data Science & ML
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit-learn", "pandas", "numpy", "spark", "hadoop", "airflow",
        "tableau", "power bi", "looker", "data visualization", "statistics",
        "nlp", "computer vision", "mlops",
        
        # Mobile
        "android", "ios", "react native", "flutter", "xamarin", "swift", "kotlin",
        
        # Testing & QA
        "selenium", "cypress", "jest", "junit", "pytest", "testing", "qa",
        "automation testing", "unit testing", "integration testing",
        
        # Methodologies
        "agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "microservices",
        "rest api", "graphql", "websocket", "grpc",
        
        # Tools
        "git", "jira", "confluence", "slack", "figma", "photoshop", "canva",
        "excel", "powerpoint", "word", "outlook",
        
        # Marketing
        "seo", "sem", "google analytics", "google ads", "facebook ads", 
        "content marketing", "social media", "email marketing", "crm",
        "hubspot", "salesforce", "mailchimp", "wordpress",
        
        # Finance
        "financial modeling", "forecasting", "budgeting", "ifrs", "gaap",
        "quickbooks", "sap", "oracle financials", "tax", "audit",
        
        # HR
        "recruitment", "talent acquisition", "onboarding", "performance management",
        "hris", "workday", "employee relations", "training", "compensation",
        
        # Soft skills
        "leadership", "communication", "teamwork", "problem solving", 
        "project management", "time management", "analytical", "creative",
        "presentation", "negotiation", "mentoring", "coaching"
    ]
    
    found_skills = set()
    for skill in all_skills:
        # Use word boundaries for better matching
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.add(normalize_skill(skill))
    
    return list(found_skills)

def calculate_experience_match(cv_years: int, required_years: int) -> Tuple[float, str]:
    """Calculate experience match score"""
    if cv_years >= required_years:
        score = min(100, 80 + (cv_years - required_years) * 5)
        status = "excellent"
    elif cv_years >= required_years - 1:
        score = 70
        status = "good"
    elif cv_years >= required_years - 2:
        score = 50
        status = "acceptable"
    else:
        score = max(20, 40 - (required_years - cv_years) * 10)
        status = "insufficient"
    
    return score, status

def extract_years_of_experience(text: str) -> int:
    """Extract years of experience from text"""
    # Pattern: "X năm", "X years", "X+ years", etc.
    patterns = [
        r"(?i)(\d{1,2})\s*\+?\s*(?:năm|years?|yrs?)",
        r"(?i)(?:kinh nghiệm|experience).*?(\d{1,2})\s*(?:năm|years?)",
        r"(?i)(\d{1,2})\s*(?:năm|years?)\s*(?:kinh nghiệm|experience)"
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        years.extend([int(m) if isinstance(m, str) else int(m[0]) for m in matches])
    
    return max(years) if years else 0

def improved_score_cv(cv_text: str, jd_text: str, language: str = "vi") -> Dict:
    """
    Improved CV scoring with better matching algorithm
    
    Returns:
        {
            "score": float (0-100),
            "breakdown": {
                "skills_match": float,
                "experience_match": float,
                "education_bonus": float,
                "language_bonus": float
            },
            "strengths": List[str],
            "weaknesses": List[str],
            "improvement_tips": List[str],
            "matched_skills": List[str],
            "missing_skills": List[str]
        }
    """
    
    # Extract skills
    cv_skills = set(extract_skills_advanced(cv_text))
    jd_skills = set(extract_skills_advanced(jd_text))
    
    # Calculate skill matching
    if not jd_skills:
        skills_score = 50  # Default if no skills in JD
        matched_skills = []
        missing_skills = []
    else:
        matched_skills = list(cv_skills & jd_skills)
        missing_skills = list(jd_skills - cv_skills)
        skills_score = (len(matched_skills) / len(jd_skills)) * 100
    
    # Extract experience
    cv_years = extract_years_of_experience(cv_text)
    jd_years = extract_years_of_experience(jd_text)
    
    if jd_years > 0:
        experience_score, exp_status = calculate_experience_match(cv_years, jd_years)
    else:
        experience_score = 50  # Default if no experience requirement
        exp_status = "unknown"
    
    # Education bonus (check for degrees)
    education_keywords = {
        "vi": ["cử nhân", "thạc sĩ", "tiến sĩ", "kỹ sư", "đại học", "bachelor", "master", "phd"],
        "en": ["bachelor", "master", "phd", "degree", "university", "college"]
    }
    
    education_score = 0
    for keyword in education_keywords.get(language, education_keywords["en"]):
        if keyword in cv_text.lower():
            education_score = 10
            break
    
    # Language bonus (check for language skills)
    language_keywords = {
        "vi": ["tiếng anh", "english", "ielts", "toeic", "toefl"],
        "en": ["bilingual", "multilingual", "fluent", "native", "proficient"]
    }
    
    language_score = 0
    for keyword in language_keywords.get(language, language_keywords["en"]):
        if keyword in cv_text.lower():
            language_score = 5
            break
    
    # Calculate final score with weighted components
    final_score = (
        skills_score * 0.60 +          # 60% weight on skills
        experience_score * 0.25 +      # 25% weight on experience
        education_score * 0.10 +       # 10% weight on education
        language_score * 0.05          # 5% weight on language
    )
    
    # Generate feedback
    strengths = []
    weaknesses = []
    improvement_tips = []
    
    if len(matched_skills) > 0:
        strengths.append(f"Matched {len(matched_skills)}/{len(jd_skills)} required skills: {', '.join(matched_skills[:10])}")
    
    if cv_years >= jd_years:
        strengths.append(f"Experience level meets requirement ({cv_years} years)")
    else:
        weaknesses.append(f"Experience below requirement ({cv_years}/{jd_years} years)")
        improvement_tips.append(f"Gain {jd_years - cv_years} more years of relevant experience" if jd_years > cv_years else "Highlight relevant experience more clearly")
    
    if len(missing_skills) > 0:
        weaknesses.append(f"Missing skills: {', '.join(missing_skills[:10])}")
        improvement_tips.append(f"Consider learning: {', '.join(missing_skills[:5])}")
    
    if skills_score < 40:
        improvement_tips.append("Expand skillset to better match job requirements")
    
    if len(matched_skills) > len(jd_skills) * 0.7:
        strengths.append("Strong skill alignment with job requirements")
    
    return {
        "score": round(final_score, 2),
        "breakdown": {
            "skills_match": round(skills_score, 2),
            "experience_match": round(experience_score, 2),
            "education_bonus": round(education_score, 2),
            "language_bonus": round(language_score, 2)
        },
        "strengths": strengths if strengths else ["Review CV to highlight relevant qualifications"],
        "weaknesses": weaknesses if weaknesses else ["No major weaknesses identified"],
        "improvement_tips": improvement_tips if improvement_tips else ["CV looks competitive for this role"],
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "metadata": {
            "cv_years_experience": cv_years,
            "jd_years_required": jd_years,
            "total_cv_skills": len(cv_skills),
            "total_jd_skills": len(jd_skills),
            "match_percentage": round((len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0, 2)
        }
    }
