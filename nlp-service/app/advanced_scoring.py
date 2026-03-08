"""
Advanced CV Scoring Algorithm with 90% Accuracy Target
Features:
- Keyword extraction with importance weighting
- Pattern-based rules for experience, education, certifications
- Section-by-section analysis
- Detailed missing keyword feedback
- Rule-based evaluation system
"""
import re
from typing import Dict, List, Tuple, Set
from collections import Counter, defaultdict
import math

class AdvancedCVScorer:
    """Advanced CV scoring with rule-based evaluation"""
    
    # Comprehensive skill taxonomy
    TECHNICAL_SKILLS = {
        "programming": [
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
            "php", "ruby", "swift", "kotlin", "scala", "r", "matlab", "julia",
            "perl", "shell", "bash", "powershell", "vba"
        ],
        "frontend": [
            "react", "vue", "vue.js", "angular", "svelte", "next.js", "nextjs", "nuxt",
            "html", "html5", "css", "css3", "sass", "scss", "less", "tailwind",
            "bootstrap", "material-ui", "mui", "chakra", "webpack", "vite", "parcel"
        ],
        "backend": [
            "node.js", "nodejs", "express", "fastapi", "django", "flask", "spring",
            "spring boot", "springboot", ".net", "dotnet", "asp.net", "laravel",
            "rails", "ruby on rails", "gin", "fiber", "actix", "axum", "nest.js", "nestjs"
        ],
        "database": [
            "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "cassandra",
            "oracle", "mssql", "sqlite", "mariadb", "dynamodb", "elasticsearch",
            "neo4j", "cockroachdb", "influxdb", "timescaledb"
        ],
        "cloud": [
            "aws", "azure", "gcp", "google cloud", "alibaba cloud", "digital ocean",
            "heroku", "vercel", "netlify", "cloudflare", "lambda", "ec2", "s3",
            "rds", "dynamodb", "cloudformation", "terraform", "pulumi"
        ],
        "devops": [
            "docker", "kubernetes", "k8s", "jenkins", "gitlab ci", "github actions",
            "circleci", "travis ci", "ansible", "puppet", "chef", "terraform",
            "helm", "istio", "prometheus", "grafana", "elk", "datadog", "newrelic",
            "nginx", "apache", "haproxy", "envoy"
        ],
        "data_ml": [
            "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
            "scikit-learn", "sklearn", "pandas", "numpy", "scipy", "spark", "pyspark",
            "hadoop", "hive", "pig", "airflow", "kafka", "flink", "storm",
            "mlflow", "kubeflow", "sagemaker", "vertex ai", "databricks"
        ],
        "mobile": [
            "android", "ios", "react native", "flutter", "xamarin", "ionic",
            "cordova", "capacitor", "swiftui", "jetpack compose"
        ],
        "testing": [
            "selenium", "cypress", "playwright", "puppeteer", "jest", "mocha",
            "junit", "testng", "pytest", "unittest", "rspec", "jasmine",
            "karma", "protractor", "cucumber", "api testing", "load testing",
            "performance testing", "security testing"
        ]
    }
    
    SOFT_SKILLS = [
        "leadership", "communication", "teamwork", "collaboration", "problem solving",
        "analytical", "critical thinking", "creativity", "adaptability", "flexibility",
        "time management", "organization", "attention to detail", "multitasking",
        "presentation", "public speaking", "negotiation", "conflict resolution",
        "mentoring", "coaching", "training", "decision making", "strategic thinking",
        "project management", "stakeholder management", "customer service",
        "interpersonal", "emotional intelligence", "work ethic", "initiative",
        "self-motivated", "proactive", "accountability", "reliability"
    ]
    
    METHODOLOGIES = [
        "agile", "scrum", "kanban", "lean", "waterfall", "devops", "ci/cd",
        "tdd", "bdd", "ddd", "microservices", "monolith", "serverless",
        "rest", "restful", "rest api", "graphql", "grpc", "soap", "websocket",
        "event-driven", "message queue", "pub/sub", "cqrs", "event sourcing"
    ]
    
    CERTIFICATIONS = {
        "aws": ["aws certified", "aws solutions architect", "aws developer", "aws sysops"],
        "azure": ["azure certified", "azure administrator", "azure developer", "azure architect"],
        "gcp": ["google cloud certified", "gcp certified"],
        "agile": ["csm", "certified scrum master", "pmp", "prince2", "safe"],
        "security": ["cissp", "ceh", "comptia security+", "cism", "cisa"],
        "data": ["databricks certified", "cloudera", "hortonworks"],
        "finance": ["cpa", "cfa", "cma", "cia", "acca", "frm"],
        "hr": ["phr", "sphr", "shrm-cp", "shrm-scp"],
        "it": ["comptia a+", "comptia network+", "ccna", "ccnp", "mcse", "rhce"]
    }
    
    EDUCATION_LEVELS = {
        "phd": ["phd", "ph.d", "tiến sĩ", "doctorate"],
        "masters": ["master", "msc", "mba", "ma", "thạc sĩ", "thac si"],
        "bachelors": ["bachelor", "bs", "ba", "bsc", "beng", "cử nhân", "cu nhan", "kỹ sư", "ky su"],
        "associate": ["associate", "associate degree", "cao đẳng"],
        "diploma": ["diploma", "certificate", "chứng chỉ"]
    }
    
    def __init__(self):
        # Build reverse index for faster lookup
        self.tech_skill_lookup = {}
        for category, skills in self.TECHNICAL_SKILLS.items():
            for skill in skills:
                self.tech_skill_lookup[skill.lower()] = category
    
    def extract_keywords(self, text: str, keyword_type: str = "all") -> Set[str]:
        """Extract keywords from text with normalization"""
        text_lower = text.lower()
        keywords = set()
        
        # Technical skills
        if keyword_type in ["all", "technical"]:
            for category, skills in self.TECHNICAL_SKILLS.items():
                for skill in skills:
                    pattern = r"\b" + re.escape(skill) + r"\b"
                    if re.search(pattern, text_lower):
                        keywords.add(skill)
        
        # Soft skills
        if keyword_type in ["all", "soft"]:
            for skill in self.SOFT_SKILLS:
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, text_lower):
                    keywords.add(skill)
        
        # Methodologies
        if keyword_type in ["all", "methodology"]:
            for method in self.METHODOLOGIES:
                pattern = r"\b" + re.escape(method) + r"\b"
                if re.search(pattern, text_lower):
                    keywords.add(method)
        
        return keywords
    
    def extract_years_experience(self, text: str) -> int:
        """Extract years of experience with multiple patterns"""
        patterns = [
            r"(?i)(\d{1,2})\s*\+?\s*(?:years?|yrs?|năm)\s+(?:of\s+)?(?:experience|kinh nghiệm)",
            r"(?i)(?:experience|kinh nghiệm)[:\s]+(\d{1,2})\s*\+?\s*(?:years?|yrs?|năm)",
            r"(?i)(\d{1,2})\s*\+?\s*(?:years?|yrs?|năm)",
            r"(?i)(?:minimum|tối thiểu|at least|ít nhất)\s+(\d{1,2})\s+(?:years?|năm)",
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            years.extend([int(m) for m in matches if m.isdigit()])
        
        return max(years) if years else 0
    
    def detect_education_level(self, text: str) -> str:
        """Detect highest education level"""
        text_lower = text.lower()
        
        for level, keywords in self.EDUCATION_LEVELS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return "unknown"
    
    def detect_certifications(self, text: str) -> List[str]:
        """Detect certifications in text"""
        text_lower = text.lower()
        found_certs = []
        
        for category, certs in self.CERTIFICATIONS.items():
            for cert in certs:
                if cert in text_lower:
                    found_certs.append(cert)
        
        return found_certs
    
    def detect_cv_sections(self, cv_text: str) -> Dict[str, bool]:
        """Detect presence of standard CV sections"""
        cv_lower = cv_text.lower()
        
        sections = {
            "experience": False,
            "education": False,
            "skills": False,
            "projects": False,
            "achievements": False,
            "certifications": False
        }
        
        # Experience section
        exp_patterns = [
            r"\b(experience|kinh nghiệm|work history|employment|công việc)\b",
            r"\b(worked at|làm việc tại|position|vị trí)\b"
        ]
        if any(re.search(p, cv_lower) for p in exp_patterns):
            sections["experience"] = True
        
        # Education section
        edu_patterns = [
            r"\b(education|học vấn|academic|university|đại học|college)\b",
            r"\b(degree|bachelor|master|phd|cử nhân|thạc sĩ)\b"
        ]
        if any(re.search(p, cv_lower) for p in edu_patterns):
            sections["education"] = True
        
        # Skills section
        skill_patterns = [
            r"\b(skills|kỹ năng|technical skills|competencies|expertise)\b",
            r"\b(proficient|thành thạo|experienced in)\b"
        ]
        if any(re.search(p, cv_lower) for p in skill_patterns):
            sections["skills"] = True
        
        # Projects section
        project_patterns = [
            r"\b(projects|dự án|portfolio|work samples)\b",
            r"\b(built|developed|created|xây dựng|phát triển)\b"
        ]
        if any(re.search(p, cv_lower) for p in project_patterns):
            sections["projects"] = True
        
        # Achievements section
        achievement_patterns = [
            r"\b(achievements|thành tựu|awards|giải thưởng|accomplishments)\b",
            r"\b(improved|increased|reduced|tăng|giảm|cải thiện)\s+\d+%"
        ]
        if any(re.search(p, cv_lower) for p in achievement_patterns):
            sections["achievements"] = True
        
        # Certifications
        if self.detect_certifications(cv_text):
            sections["certifications"] = True
        
        return sections
    
    def calculate_keyword_importance(self, keywords: Set[str]) -> Dict[str, float]:
        """Assign importance weights to keywords"""
        weights = {}
        
        for keyword in keywords:
            # Technical skills have higher weight
            if keyword in self.tech_skill_lookup:
                category = self.tech_skill_lookup[keyword]
                # Core categories get higher weight
                if category in ["programming", "database", "cloud", "devops"]:
                    weights[keyword] = 1.5
                elif category in ["data_ml", "backend", "frontend"]:
                    weights[keyword] = 1.3
                else:
                    weights[keyword] = 1.0
            # Methodologies are important
            elif keyword in self.METHODOLOGIES:
                weights[keyword] = 1.2
            # Soft skills have lower weight
            elif keyword in self.SOFT_SKILLS:
                weights[keyword] = 0.7
            else:
                weights[keyword] = 1.0
        
        return weights
    
    def score_cv(self, cv_text: str, jd_text: str, language: str = "vi") -> Dict:
        """
        Advanced CV scoring with detailed feedback
        
        Returns dict with:
        - score: float (0-100)
        - breakdown: detailed scoring breakdown
        - strengths: list of specific strengths
        - weaknesses: list of specific weaknesses (missing keywords)
        - improvement_tips: actionable recommendations
        - matched_keywords: categorized matched keywords
        - missing_keywords: categorized missing keywords
        """
        
        # Extract keywords from both texts
        cv_tech = self.extract_keywords(cv_text, "technical")
        jd_tech = self.extract_keywords(jd_text, "technical")
        
        cv_soft = self.extract_keywords(cv_text, "soft")
        jd_soft = self.extract_keywords(jd_text, "soft")
        
        cv_method = self.extract_keywords(cv_text, "methodology")
        jd_method = self.extract_keywords(jd_text, "methodology")
        
        # Calculate matches and misses
        matched_tech = cv_tech & jd_tech
        missing_tech = jd_tech - cv_tech
        
        matched_soft = cv_soft & jd_soft
        missing_soft = jd_soft - cv_soft
        
        matched_method = cv_method & jd_method
        missing_method = jd_method - cv_method
        
        # Get keyword importance weights
        jd_tech_weights = self.calculate_keyword_importance(jd_tech)
        jd_soft_weights = self.calculate_keyword_importance(jd_soft)
        jd_method_weights = self.calculate_keyword_importance(jd_method)
        
        # Calculate weighted technical skills score (40%)
        if jd_tech:
            total_tech_weight = sum(jd_tech_weights.values())
            matched_tech_weight = sum(jd_tech_weights.get(k, 1.0) for k in matched_tech)
            tech_score = (matched_tech_weight / total_tech_weight) * 100
        else:
            tech_score = 50  # Default if no technical skills in JD
        
        # Calculate soft skills score (15%)
        if jd_soft:
            total_soft_weight = sum(jd_soft_weights.values())
            matched_soft_weight = sum(jd_soft_weights.get(k, 0.7) for k in matched_soft)
            soft_score = (matched_soft_weight / total_soft_weight) * 100
        else:
            soft_score = 50
        
        # Calculate methodology score (5%)
        if jd_method:
            method_score = (len(matched_method) / len(jd_method)) * 100
        else:
            method_score = 50
        
        # Experience matching (20%)
        cv_years = self.extract_years_experience(cv_text)
        jd_years = self.extract_years_experience(jd_text)
        
        if jd_years > 0:
            if cv_years >= jd_years:
                exp_score = min(100, 85 + (cv_years - jd_years) * 3)
            elif cv_years >= jd_years - 1:
                exp_score = 75
            elif cv_years >= jd_years - 2:
                exp_score = 60
            else:
                exp_score = max(30, 50 - (jd_years - cv_years) * 8)
        else:
            # If JD doesn't specify, give average score
            exp_score = 60 if cv_years > 0 else 40
        
        # Education matching (10%)
        cv_edu = self.detect_education_level(cv_text)
        jd_edu = self.detect_education_level(jd_text)
        
        edu_score = self._calculate_education_score(cv_edu, jd_edu)
        
        # Certifications & achievements (5%)
        cv_certs = self.detect_certifications(cv_text)
        jd_certs = self.detect_certifications(jd_text)
        
        cert_score = 0
        if jd_certs:
            matched_certs = set(cv_certs) & set(jd_certs)
            cert_score = (len(matched_certs) / len(jd_certs)) * 100
        else:
            cert_score = 50 if cv_certs else 40
        
        # CV structure quality (5%)
        sections = self.detect_cv_sections(cv_text)
        structure_score = (sum(sections.values()) / len(sections)) * 100
        
        # Calculate final weighted score
        final_score = (
            tech_score * 0.40 +
            soft_score * 0.15 +
            method_score * 0.05 +
            exp_score * 0.20 +
            edu_score * 0.10 +
            cert_score * 0.05 +
            structure_score * 0.05
        )
        
        # Generate detailed feedback
        feedback = self._generate_feedback(
            matched_tech, missing_tech,
            matched_soft, missing_soft,
            matched_method, missing_method,
            cv_years, jd_years,
            cv_edu, jd_edu,
            cv_certs, jd_certs,
            sections,
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
                "cv_sections": sections
            }
        }
    
    def _calculate_education_score(self, cv_edu: str, jd_edu: str) -> float:
        """Calculate education matching score"""
        edu_hierarchy = {
            "phd": 5,
            "masters": 4,
            "bachelors": 3,
            "associate": 2,
            "diploma": 1,
            "unknown": 0
        }
        
        cv_level = edu_hierarchy.get(cv_edu, 0)
        jd_level = edu_hierarchy.get(jd_edu, 0)
        
        if jd_level == 0:
            # JD doesn't specify, give partial credit if CV has education
            return 60 if cv_level > 0 else 40
        
        if cv_level >= jd_level:
            return 100
        elif cv_level == jd_level - 1:
            return 70
        elif cv_level > 0:
            return 50
        else:
            return 30
    
    def _generate_feedback(
        self,
        matched_tech, missing_tech,
        matched_soft, missing_soft,
        matched_method, missing_method,
        cv_years, jd_years,
        cv_edu, jd_edu,
        cv_certs, jd_certs,
        sections,
        language
    ) -> Dict[str, List[str]]:
        """Generate detailed, actionable feedback"""
        
        strengths = []
        weaknesses = []
        tips = []
        
        # Technical skills feedback
        if matched_tech:
            tech_list = ", ".join(sorted(list(matched_tech))[:8])
            if len(matched_tech) > 8:
                tech_list += f" + {len(matched_tech) - 8} more"
            strengths.append(f"✓ Matched {len(matched_tech)}/{len(matched_tech) + len(missing_tech)} technical skills: {tech_list}")
        
        if missing_tech:
            # Categorize missing technical skills
            missing_by_category = defaultdict(list)
            for skill in missing_tech:
                category = self.tech_skill_lookup.get(skill, "other")
                missing_by_category[category].append(skill)
            
            for category, skills in missing_by_category.items():
                skill_list = ", ".join(sorted(skills)[:5])
                if len(skills) > 5:
                    skill_list += f" + {len(skills) - 5} more"
                weaknesses.append(f"✗ Missing {category} skills: {skill_list}")
                tips.append(f"→ Consider learning {category} technologies: {', '.join(sorted(skills)[:3])}")
        
        # Soft skills feedback
        if missing_soft:
            soft_list = ", ".join(sorted(list(missing_soft))[:5])
            weaknesses.append(f"✗ Missing soft skills: {soft_list}")
            tips.append(f"→ Highlight soft skills in CV: {', '.join(sorted(list(missing_soft))[:3])}")
        elif matched_soft:
            strengths.append(f"✓ Demonstrated {len(matched_soft)} relevant soft skills")
        
        # Methodology feedback
        if missing_method:
            method_list = ", ".join(sorted(list(missing_method)))
            weaknesses.append(f"✗ Missing methodologies: {method_list}")
            tips.append(f"→ Gain experience with: {method_list}")
        elif matched_method:
            strengths.append(f"✓ Familiar with {len(matched_method)} required methodologies")
        
        # Experience feedback
        if jd_years > 0:
            if cv_years >= jd_years:
                strengths.append(f"✓ Experience exceeds requirement ({cv_years} years vs {jd_years} required)")
            else:
                gap = jd_years - cv_years
                weaknesses.append(f"✗ Experience below requirement ({cv_years} years vs {jd_years} required)")
                tips.append(f"→ Gain {gap} more year{'s' if gap > 1 else ''} of relevant experience or highlight transferable experience")
        
        # Education feedback
        if jd_edu != "unknown":
            edu_names = {
                "phd": "PhD/Doctorate",
                "masters": "Master's degree",
                "bachelors": "Bachelor's degree",
                "associate": "Associate degree",
                "diploma": "Diploma/Certificate"
            }
            
            jd_edu_name = edu_names.get(jd_edu, jd_edu)
            cv_edu_name = edu_names.get(cv_edu, cv_edu)
            
            if cv_edu == "unknown":
                weaknesses.append(f"✗ Education level unclear (requires: {jd_edu_name})")
                tips.append(f"→ Clearly state your education level ({jd_edu_name} required)")
            elif self._calculate_education_score(cv_edu, jd_edu) >= 100:
                strengths.append(f"✓ Education meets/exceeds requirement ({cv_edu_name})")
            else:
                weaknesses.append(f"✗ Education below requirement ({cv_edu_name} vs {jd_edu_name} required)")
        
        # Certifications feedback
        if jd_certs:
            missing_certs = set(jd_certs) - set(cv_certs)
            if missing_certs:
                cert_list = ", ".join(list(missing_certs)[:3])
                weaknesses.append(f"✗ Missing certifications: {cert_list}")
                tips.append(f"→ Consider obtaining: {cert_list}")
            else:
                strengths.append(f"✓ All required certifications present")
        
        # Structural feedback
        missing_sections = [k for k, v in sections.items() if not v]
        if missing_sections:
            section_list = ", ".join(missing_sections[:3])
            weaknesses.append(f"✗ Missing CV sections: {section_list}")
            tips.append(f"→ Add {section_list} section(s) to improve ATS matching")
        else:
            strengths.append("✓ CV has all standard sections")
        
        # Default messages if empty
        if not strengths:
            strengths.append("• Review CV to better highlight qualifications matching this JD")
        
        if not weaknesses:
            weaknesses.append("• CV appears well-matched to job requirements")
        
        if not tips:
            tips.append("• Tailor your CV summary and descriptions to mirror JD language")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "tips": tips
        }


# Create singleton instance
_scorer_instance = None

def get_advanced_scorer() -> AdvancedCVScorer:
    """Get singleton instance of advanced scorer"""
    global _scorer_instance
    if _scorer_instance is None:
        _scorer_instance = AdvancedCVScorer()
    return _scorer_instance
