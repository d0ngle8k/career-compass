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
from typing import Any, Dict, List, Tuple, Set
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
        "express": ["fastapi", "flask", "django", "nest.js", "nestjs"],
        "fastapi": ["express", "flask", "django", "spring boot"],
        "django": ["fastapi", "flask", "rails", "spring boot"],
        "flask": ["fastapi", "django", "express"],
        "spring boot": ["spring", "nest.js", "nestjs", "express", "fastapi"],
        "nest.js": ["nestjs", "express", "spring boot"],
        "nestjs": ["nest.js", "express", "spring boot"],
        
        # Databases - SQL
        "postgresql": ["mysql", "mariadb", "postgres", "sql"],
        "postgres": ["postgresql", "mysql", "mariadb", "sql"],
        "mysql": ["postgresql", "mariadb", "sql"],
        "mariadb": ["mysql", "postgresql", "sql"],
        "sql": ["postgresql", "mysql", "mariadb"],
        
        # Databases - NoSQL
        "mongodb": ["dynamodb", "cassandra", "cosmosdb", "couchdb"],
        "cassandra": ["mongodb", "dynamodb", "scylladb"],
        "dynamodb": ["mongodb", "cassandra"],
        "redis": ["memcached", "elasticache"],
        
        # Cloud providers - AWS
        "aws": ["azure", "gcp", "google cloud"],
        "ec2": ["azure vm", "gcp compute"],
        "s3": ["azure blob", "gcp storage"],
        "lambda": ["azure functions", "gcp functions"],
        "rds": ["azure sql", "gcp sql"],
        
        # Cloud providers - Azure
        "azure": ["aws", "gcp"],
        "azure vm": ["ec2", "gcp compute"],
        "azure blob": ["s3", "gcp storage"],
        "azure functions": ["lambda", "gcp functions"],
        
        # Cloud providers - GCP
        "gcp": ["aws", "azure", "google cloud"],
        "google cloud": ["gcp", "aws", "azure"],
        "gcp compute": ["ec2", "azure vm"],
        "gcp storage": ["s3", "azure blob"],
        "gcp functions": ["lambda", "azure functions"],
        
        # Infrastructure as Code
        "terraform": ["cloudformation", "pulumi", "ansible"],
        "cloudformation": ["terraform", "pulumi"],
        "pulumi": ["terraform", "cloudformation"],
        "ansible": ["terraform", "puppet", "chef"],
        
        # Container orchestration
        "kubernetes": ["k8s", "docker swarm", "nomad", "openshift"],
        "k8s": ["kubernetes", "docker swarm", "openshift"],
        "docker": ["podman", "containerd"],
        "openshift": ["kubernetes", "k8s"],
        
        # CI/CD
        "jenkins": ["github actions", "gitlab ci", "circleci", "travis ci"],
        "github actions": ["gitlab ci", "jenkins", "circleci"],
        "gitlab ci": ["github actions", "jenkins", "circleci"],
        "circleci": ["github actions", "gitlab ci", "jenkins"],
        
        # Programming languages - Similar paradigms
        "javascript": ["typescript"],
        "typescript": ["javascript"],
        "python": ["ruby", "go"],
        "java": ["c#", "kotlin", "scala"],
        "c#": ["java", "f#"],
        "go": ["rust", "python"],
        "rust": ["go", "c++"],
        
        # Message Queues
        "kafka": ["rabbitmq", "sqs", "redis", "nats"],
        "rabbitmq": ["kafka", "sqs", "activemq"],
        "sqs": ["kafka", "rabbitmq"],
        
        # Methodologies
        "agile": ["scrum", "kanban"],
        "scrum": ["agile", "kanban"],
        "kanban": ["agile", "scrum"],
        "rest": ["restful", "rest api", "graphql"],
        "restful": ["rest", "rest api"],
        "rest api": ["rest", "restful", "api"],
        "graphql": ["rest", "restful"],
        
        # Testing frameworks
        "jest": ["mocha", "jasmine", "vitest"],
        "pytest": ["unittest", "nose"],
        "junit": ["testng", "mockito"],
    }
    
    # Soft skills that can be inferred from experience descriptions
    SOFT_SKILL_CONTEXTS = {
        "leadership": [
            r"(?i)\b(led|leading|lead|dẫn dắt|lãnh đạo|chỉ đạo)\s+(a\s+|the\s+)?(team|nhóm|đội)",
            r"(?i)\b(managed?|managing|quản lý)\s+\d+\s*(people|developers|engineers|members|người|nhân viên|thành viên)",
            r"(?i)\b(mentor|mentored|mentoring|hướng dẫn|đào tạo)",
            r"(?i)\b(supervised?|supervising|giám sát)",
            r"(?i)\bleadership\s+(role|position|experience)",
            r"(?i)\b(built|created|xây dựng)\s+(a\s+|the\s+)?(team|nhóm)",
        ],
        "teamwork": [
            r"(?i)\b(collaborated?|collaborating|cộng tác|hợp tác)\s+(with|cùng|với)",
            r"(?i)\b(worked?|working|làm việc)\s+(with|in|cùng|trong)\s+(a\s+|the\s+)?(team|nhóm|đội)",
            r"(?i)\bcross-functional\s+team",
            r"(?i)\bteam\s+(player|member|work|effort|collaboration)",
            r"(?i)\b(cooperation|phối hợp)",
        ],
        "communication": [
            r"(?i)\b(presented?|presenting|trình bày|báo cáo)\s+(to|at|cho|tại|với)",
            r"(?i)\b(communicated?|communicating|giao tiếp|trao đổi)\s+(with|to|về|với)",
            r"(?i)\bstakeholder\s+(management|communication|engagement)",
            r"(?i)\b(documented?|documenting|tài liệu)",
            r"(?i)\b(reported?|reporting)\s+to",
            r"(?i)\b(public|presentation)\s+skill",
        ],
        "problem solving": [
            r"(?i)\b(solved?|solving|resolved?|resolving|giải quyết|xử lý)\s+(complex\s+)?(problems?|issues?|vấn đề)",
            r"(?i)\b(debugged?|debugging|fix|fixed)",
            r"(?i)\b(troubleshot|troubleshooting)",
            r"(?i)\b(optimized?|optimizing|improved?|tối ưu|cải thiện)\s+(performance|system|process)",
            r"(?i)\b(innovative|sáng tạo)\s+(solution|approach)",
        ],
        "analytical": [
            r"(?i)\b(analyzed?|analyzing|analysed?|analysing|phân tích)",
            r"(?i)\b(evaluated?|evaluating|đánh giá)",
            r"(?i)\b(assessed?|assessing)",
            r"(?i)\bdata-driven",
            r"(?i)\b(metrics|KPI|measurement)",
        ],
        "project management": [
            r"(?i)\b(managed?|managing|quản lý)\s+(projects?|initiatives?|dự án)",
            r"(?i)\b(coordinated?|coordinating|điều phối)",
            r"(?i)\b(planned?|planning|lập kế hoạch)\s+and\s+(executed?|implementing|execution)",
            r"(?i)\bproject\s+(manager|lead|coordinator)",
            r"(?i)\bagile|scrum\s+(master|lead)",
        ],
        "adaptability": [
            r"(?i)\b(adapted?|adapting|thích nghi)",
            r"(?i)\b(flexible|flexibility|linh hoạt)",
            r"(?i)\b(quick\s+learner|fast\s+learner)",
            r"(?i)\b(learned?|learning)\s+(new|quickly)",
        ],
        "self-motivated": [
            r"(?i)\b(self-motivated|proactive|chủ động|tự giác)",
            r"(?i)\b(initiative|sáng kiến)",
            r"(?i)\b(independent|independently|độc lập)",
            r"(?i)\btook\s+initiative",
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
                bonus = min(15, len(extra_skills) * 2.5)
                tech_score = min(100, tech_score + bonus)
        else:
            tech_score = 70  # Default if no technical skills in JD
        
        # Calculate soft skills score
        if jd_soft:
            soft_score = (len(matched_soft) / len(jd_soft)) * 100
            # Bonus for having more soft skills than required
            if len(matched_soft) >= len(jd_soft) * 0.6:
                soft_score = min(100, soft_score + 15)
            # Give base credit if any soft skills found
            if matched_soft:
                soft_score = max(soft_score, 40)
        else:
            soft_score = 70 if cv_soft else 60
        
        # Calculate methodology score with related skills
        if jd_method:
            total_method_match = sum(method_matches.values())
            method_score = (total_method_match / len(jd_method)) * 100
            # Give base credit if any methodologies found
            if method_score > 0:
                method_score = max(method_score, 50)
        else:
            method_score = 70
        
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
            # Give partial credit for having any certs even if not exact match
            if not matched_certs and cv_certs:
                cert_score = 40
        else:
            cert_score = 70 if cv_certs else 60
        
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
        
        # Apply baseline floor - any complete CV gets at least these minimums
        if structure_score >= 80:  # Has most standard sections
            final_score = max(50, final_score)
        elif structure_score >= 60:
            final_score = max(45, final_score)
        else:
            final_score = max(40, final_score)
        
        breakdown_scores = {
            "technical_skills": round(tech_score, 2),
            "soft_skills": round(soft_score, 2),
            "methodologies": round(method_score, 2),
            "experience": round(exp_score, 2),
            "education": round(edu_score, 2),
            "certifications": round(cert_score, 2),
            "structure": round(structure_score, 2)
        }

        # Generate detailed feedback based on score band and weak components
        feedback = self._generate_enhanced_feedback(
            matched_tech, missing_tech, tech_matches,
            matched_soft, missing_soft, cv_soft_inferred,
            matched_method, missing_method,
            cv_years, jd_years,
            cv_edu, jd_edu,
            cv_certs, jd_certs,
            sections,
            field,
            language,
            final_score,
            breakdown_scores
        )
        
        return {
            "score": round(final_score, 2),
            "breakdown": breakdown_scores,
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
        language,
        final_score,
        breakdown_scores
    ) -> Dict[str, List[str]]:
        """Generate detailed, deterministic feedback driven by score bands and component gaps."""

        strengths: List[str] = [self._score_band_summary(final_score, language)]
        weaknesses: List[str] = []

        gap_metrics = self._derive_gap_metrics(
            matched_tech,
            missing_tech,
            matched_soft,
            missing_soft,
            matched_method,
            missing_method,
            cv_years,
            jd_years,
            cv_certs,
            jd_certs,
            sections,
        )
        ranked_components = self._rank_weak_components(breakdown_scores)

        # Strengths: keep concise, evidence-based.
        if gap_metrics["total_tech_required"] > 0:
            strengths.append(
                f"Độ khớp kỹ năng kỹ thuật đạt {gap_metrics['tech_match_rate']:.1f}% "
                f"({gap_metrics['matched_tech_count']}/{gap_metrics['total_tech_required']})"
            )

        if jd_years > 0:
            if cv_years >= jd_years:
                strengths.append(f"Kinh nghiệm đáp ứng JD: {cv_years:.1f} năm so với yêu cầu {jd_years:.1f} năm")
            else:
                strengths.append(f"Kinh nghiệm hiện có: {cv_years:.1f} năm (cần thêm {max(0.0, jd_years - cv_years):.1f} năm)")

        present_sections = [self._section_label(k) for k, v in sections.items() if v]
        strengths.append(f"CV có {len(present_sections)} mục chính đã nhận diện: {', '.join(sorted(present_sections)[:4])}")

        # Weaknesses with 3-part structure: issue + evidence + impact.
        if gap_metrics["missing_tech_count"] > 0:
            weaknesses.append(
                self._render_detailed_weakness(
                    "Thiếu kỹ năng kỹ thuật cốt lõi so với JD",
                    (
                        f"Thiếu {gap_metrics['missing_tech_count']} kỹ năng; "
                        f"mức khớp kỹ năng kỹ thuật {gap_metrics['tech_match_rate']:.1f}% "
                        f"({gap_metrics['matched_tech_count']}/{gap_metrics['total_tech_required']}); "
                        f"ưu tiên thiếu: {', '.join(gap_metrics['missing_tech_top']) if gap_metrics['missing_tech_top'] else 'N/A'}"
                    ),
                    "Giảm điểm kỹ năng kỹ thuật và khả năng qua vòng lọc ATS theo từ khóa"
                )
            )

        if gap_metrics["experience_gap"] > 0:
            weaknesses.append(
                self._render_detailed_weakness(
                    "Khoảng cách kinh nghiệm so với JD",
                    (
                        f"CV {cv_years:.1f} năm, JD yêu cầu {jd_years:.1f} năm; "
                        f"thiếu {gap_metrics['experience_gap']:.1f} năm"
                    ),
                    "Giảm mức phù hợp ở tiêu chí seniority, có thể bị loại ở vòng đầu"
                )
            )

        if gap_metrics["missing_sections_count"] > 0:
            weaknesses.append(
                self._render_detailed_weakness(
                    "Thiếu mục quan trọng trong CV",
                    (
                        f"Thiếu {gap_metrics['missing_sections_count']} mục: "
                        f"{', '.join(gap_metrics['missing_sections_top']) if gap_metrics['missing_sections_top'] else 'N/A'}"
                    ),
                    "Khả năng phân tích CV của ATS kém ổn định và nhà tuyển dụng khó xác thực năng lực nhanh"
                )
            )

        if gap_metrics["cert_gap"] > 0:
            weaknesses.append(
                self._render_detailed_weakness(
                    "Thiếu chứng chỉ JD ưu tiên",
                    (
                        f"JD yêu cầu/ưu tiên {gap_metrics['jd_cert_count']} chứng chỉ, "
                        f"CV đáp ứng {gap_metrics['cv_cert_match_count']}, thiếu {gap_metrics['cert_gap']}"
                    ),
                    "Giảm lợi thế cạnh tranh ở vòng shortlist khi so với ứng viên tương đương"
                )
            )

        # Component-level weaknesses from weakest areas.
        component_impact = {
            "technical_skills": "Điểm match tổng thể khó vượt ngưỡng shortlist nếu không tăng độ phủ kỹ năng chính",
            "soft_skills": "Bullet thiếu năng lực phối hợp/ảnh hưởng, giảm thuyết phục ở vòng phỏng vấn hành vi",
            "methodologies": "Thiếu tín hiệu quy trình làm việc chuẩn, ảnh hưởng đánh giá mức chuyên nghiệp",
            "experience": "Khó chứng minh độ chín nghề nghiệp cho role mục tiêu",
            "education": "Giảm độ tin cậy hồ sơ ở các role có tiêu chí học vấn rõ",
            "certifications": "Mất điểm cộng ở vị trí yêu cầu chuẩn hóa kiến thức",
            "structure": "CV khó đọc và khó scan tự động, làm giảm tỷ lệ được đọc sâu",
        }
        for comp, comp_score, severity in ranked_components[:3]:
            if comp_score >= 70:
                continue
            weaknesses.append(
                self._render_detailed_weakness(
                    f"Thành phần {self._component_label(comp)} ở mức {self._severity_label(severity)}",
                    f"Điểm {self._component_label(comp)} = {comp_score:.1f}/100",
                    component_impact.get(comp, "Giảm tổng điểm phù hợp và giảm xác suất được mời phỏng vấn")
                )
            )

        # Deduplicate while preserving order.
        dedup_weaknesses: List[str] = []
        seen_weaknesses = set()
        for item in weaknesses:
            if item not in seen_weaknesses:
                dedup_weaknesses.append(item)
                seen_weaknesses.add(item)
        weaknesses = dedup_weaknesses

        # Ensure >= 3 weaknesses with quantitative evidence.
        if len(weaknesses) < 3:
            for comp, comp_score, severity in ranked_components:
                fallback = self._render_detailed_weakness(
                    f"Thành phần {self._component_label(comp)} ở mức {self._severity_label(severity)}",
                    f"Điểm hiện tại {comp_score:.1f}/100",
                    "Làm giảm tổng điểm phù hợp và mức cạnh tranh của hồ sơ"
                )
                if fallback not in weaknesses:
                    weaknesses.append(fallback)
                if len(weaknesses) >= 3:
                    break

        tips = self._build_priority_actions(
            final_score,
            field,
            language,
            gap_metrics,
            ranked_components,
        )
        tips.extend(self._score_band_tips(final_score, language))

        # Guardrails for meaningless/generic output.
        cleaned_tips: List[str] = []
        for tip in tips:
            low = tip.lower()
            if "cải thiện đáng kể" in low and "Bằng chứng" not in tip:
                continue
            cleaned_tips.append(tip)

        # Deduplicate and clamp 3-5 tips.
        dedup_tips: List[str] = []
        seen_tips = set()
        for item in cleaned_tips:
            if item not in seen_tips:
                dedup_tips.append(item)
                seen_tips.add(item)
        tips = dedup_tips

        if len(tips) < 3:
            tips.extend([
                "P1 (24h) - Đồng bộ top 10 từ khóa xuất hiện nhiều nhất trong JD vào Summary và Skills; đầu ra: độ phủ từ khóa >= 80%.",
                "P2 (3-7 ngày) - Viết lại 3 bullet mạnh nhất theo công thức Hành động + Chỉ số + Tác động; đầu ra: mỗi bullet có ít nhất 1 metric.",
                "P3 (sau ngưỡng) - Tùy chỉnh CV theo từng JD thay vì một bản dùng chung; đầu ra: tăng tỷ lệ phản hồi phỏng vấn.",
            ])

        return {
            "strengths": strengths[:6],
            "weaknesses": weaknesses[:8],
            "tips": tips[:5]
        }

    def _derive_gap_metrics(
        self,
        matched_tech,
        missing_tech,
        matched_soft,
        missing_soft,
        matched_method,
        missing_method,
        cv_years,
        jd_years,
        cv_certs,
        jd_certs,
        sections,
    ) -> Dict[str, Any]:
        """Derive stable, numeric gap metrics used by feedback policies."""
        matched_tech_count = len(matched_tech)
        missing_tech_count = len(missing_tech)
        total_tech_required = matched_tech_count + missing_tech_count
        tech_match_rate = (matched_tech_count / total_tech_required * 100) if total_tech_required > 0 else 0.0

        matched_soft_count = len(matched_soft)
        missing_soft_count = len(missing_soft)
        total_soft_required = matched_soft_count + missing_soft_count
        soft_match_rate = (matched_soft_count / total_soft_required * 100) if total_soft_required > 0 else 0.0

        experience_gap = max(0.0, float(jd_years) - float(cv_years)) if jd_years > 0 else 0.0

        jd_cert_set = {str(c).strip().lower() for c in jd_certs if str(c).strip()}
        cv_cert_set = {str(c).strip().lower() for c in cv_certs if str(c).strip()}
        cert_gap_set = jd_cert_set - cv_cert_set

        missing_sections = sorted([self._section_label(k) for k, v in sections.items() if not v])

        return {
            "matched_tech_count": matched_tech_count,
            "missing_tech_count": missing_tech_count,
            "total_tech_required": total_tech_required,
            "tech_match_rate": tech_match_rate,
            "missing_tech_top": sorted(list(missing_tech))[:5],
            "matched_soft_count": matched_soft_count,
            "missing_soft_count": missing_soft_count,
            "soft_match_rate": soft_match_rate,
            "missing_soft_top": sorted(list(missing_soft))[:4],
            "matched_method_count": len(matched_method),
            "missing_method_count": len(missing_method),
            "missing_method_top": sorted(list(missing_method))[:4],
            "experience_gap": experience_gap,
            "missing_sections_count": len(missing_sections),
            "missing_sections_top": missing_sections[:4],
            "jd_cert_count": len(jd_cert_set),
            "cv_cert_match_count": len(jd_cert_set & cv_cert_set),
            "cert_gap": len(cert_gap_set),
        }

    def _rank_weak_components(self, breakdown_scores: Dict[str, float]) -> List[Tuple[str, float, str]]:
        """Rank weak components by severity for deterministic planning."""
        ranked: List[Tuple[str, float, str]] = []
        for comp, score in sorted(breakdown_scores.items(), key=lambda x: x[1]):
            if score < 40:
                severity = "critical"
            elif score < 60:
                severity = "high"
            elif score < 75:
                severity = "medium"
            else:
                severity = "low"
            ranked.append((comp, float(score), severity))
        return ranked

    def _build_priority_actions(
        self,
        final_score: float,
        field: str,
        language: str,
        gap_metrics: Dict[str, Any],
        ranked_components: List[Tuple[str, float, str]],
    ) -> List[str]:
        """Build actionable P1/P2/P3 plan from score band + gap severities."""
        _ = str(language).lower()
        tips: List[str] = []

        # P1: highest-impact fixes in 24h.
        p1_actions: List[str] = []
        if gap_metrics["missing_tech_count"] > 0:
            top_tech = ', '.join(gap_metrics["missing_tech_top"][:3])
            p1_actions.append(
                f"Lấp top kỹ năng thiếu: {top_tech if top_tech else 'N/A'}"
            )
        if gap_metrics["missing_sections_count"] > 0:
            top_sections = ', '.join(gap_metrics["missing_sections_top"][:2])
            p1_actions.append(
                f"Bổ sung mục bắt buộc: {top_sections if top_sections else 'kinh nghiệm, kỹ năng'}"
            )
        if not p1_actions and ranked_components:
            p1_actions.append(f"Tối ưu component yếu nhất: {self._component_label(ranked_components[0][0])}")

        tips.append(
            "P1 (24h) - "
            + " + ".join(p1_actions[:2])
            + "; Đầu ra: tăng rõ điểm ở component yếu nhất và CV đủ section cốt lõi."
        )

        # P2: structured rewrite in 3-7 days.
        p2_focus = []
        if gap_metrics["experience_gap"] > 0:
            p2_focus.append(
                f"viết lại phần kinh nghiệm để bù thiếu {gap_metrics['experience_gap']:.1f} năm bằng tác động/độ phức tạp"
            )
        if gap_metrics["missing_soft_count"] > 0:
            p2_focus.append(
                f"thể hiện {', '.join(gap_metrics['missing_soft_top'][:2])} qua bullet có số liệu"
            )
        if gap_metrics["cert_gap"] > 0:
            p2_focus.append("nêu chứng chỉ đang có hoặc kế hoạch thi chứng chỉ liên quan JD")
        if not p2_focus:
            p2_focus.append("chuẩn hóa 5 bullet thành định dạng Hành động + Chỉ số + Tác động")

        tips.append(
            "P2 (3-7 ngày) - "
            + "; ".join(p2_focus[:3])
            + "; Đầu ra: mỗi bullet chính có số liệu cụ thể và ngôn ngữ bám JD."
        )

        # P3: after threshold is reached.
        score_target = 95 if final_score >= 90 else 90 if final_score >= 80 else 80 if final_score >= 70 else 70 if final_score >= 60 else 60
        p3_text = (
            f"P3 (sau ngưỡng) - Tối ưu CV theo từng JD để đạt mốc {score_target}+; "
            "Đầu ra: tăng tỷ lệ vào danh sách rút gọn/phỏng vấn nhờ bản CV chuyên biệt theo vị trí."
        )
        tips.append(p3_text)

        # Field-aware actionable add-on.
        if field == "software" and gap_metrics["missing_tech_count"] > 0:
            tips.append(
                "P2 (software) - Thêm 1 dự án minh họa cho mỗi kỹ năng thiếu quan trọng; Đầu ra: có bằng chứng năng lực qua liên kết GitHub/portfolio."
            )
        elif field in ["marketing", "hr"]:
            tips.append(
                "P2 (marketing/hr) - Mỗi bullet cần KPI định lượng (conversion, retention, engagement...); Đầu ra: kỹ năng mềm được chứng minh bằng số liệu."
            )

        # Guardrail: avoid long upskilling advice for high bands.
        if final_score < 50:
            tips.append(
                "P3 (nâng nền) - Lập lộ trình nâng cấp kỹ năng 6-8 tuần theo 2 kỹ năng cốt lõi nhất từ JD; Đầu ra: có dự án minh chứng trước khi ứng tuyển lại."
            )

        return tips

    def _render_detailed_weakness(self, issue: str, evidence: str, impact: str) -> str:
        """Render weakness with mandatory 3-part structure."""
        return f"{issue}. Bằng chứng: {evidence}. Tác động: {impact}."

    def _component_label(self, component_key: str) -> str:
        labels = {
            "technical_skills": "kỹ năng kỹ thuật",
            "soft_skills": "kỹ năng mềm",
            "methodologies": "phương pháp làm việc",
            "experience": "kinh nghiệm",
            "education": "học vấn",
            "certifications": "chứng chỉ",
            "structure": "cấu trúc CV",
        }
        return labels.get(component_key, component_key)

    def _severity_label(self, severity: str) -> str:
        labels = {
            "critical": "nghiêm trọng",
            "high": "cao",
            "medium": "trung bình",
            "low": "thấp",
        }
        return labels.get(str(severity).lower(), str(severity))

    def _section_label(self, section_key: str) -> str:
        labels = {
            "summary": "tóm tắt",
            "skills": "kỹ năng",
            "experience": "kinh nghiệm",
            "projects": "dự án",
            "education": "học vấn",
            "certifications": "chứng chỉ",
            "achievements": "thành tích",
            "awards": "giải thưởng",
            "activities": "hoạt động",
            "contact": "thông tin liên hệ",
        }
        return labels.get(str(section_key).lower(), str(section_key))

    def _score_band_summary(
        self,
        final_score: float,
        language: str,
    ) -> str:
        """Generate detailed score band summary with actionable context"""
        _ = str(language).lower()
        if final_score >= 90:
            return f"✨ PHÙ HỢP XUẤT SẮC ({final_score:.1f}/100): CV khớp hầu hết yêu cầu JD - Rất có khả năng vượt vòng sơ tuyển ATS"
        elif final_score >= 80:
            return f"⭐ PHÙ HỢP CAO ({final_score:.1f}/100): CV khớp tốt với JD - Có cơ hội cao được mời phỏng vấn nếu tối ưu thêm một số điểm"
        elif final_score >= 70:
            return f"✓ PHÙ HỢP KHÁ ({final_score:.1f}/100): CV có nền tảng tốt - Cần bổ sung một số kỹ năng quan trọng để tăng cạnh tranh"
        elif final_score >= 60:
            return f"△ PHÙ HỢP TRUNG BÌNH ({final_score:.1f}/100): CV đáp ứng một phần yêu cầu - Cần cải thiện đáng kể để có cơ hội"
        elif final_score >= 50:
            return f"⚠ PHÙ HỢP THẤP ({final_score:.1f}/100): CV còn thiếu nhiều yêu cầu cốt lõi - Nguy cơ cao bị loại bởi ATS"
        else:
            return f"✗ PHÙ HỢP RẤT THẤP ({final_score:.1f}/100): CV chưa khớp với JD này - Nên cân nhắc vị trí phù hợp hơn hoặc học thêm kỹ năng"

    def _score_band_tips(self, final_score: float, language: str) -> List[str]:
        """Generate concise score-band strategy without generic wording."""
        _ = str(language).lower()
        if final_score >= 90:
            return [
                "Chiến lược 90+: tinh chỉnh ngôn ngữ bám JD và thêm 1 bằng chứng tác động nổi bật ngay phần đầu CV.",
            ]
        elif final_score >= 80:
            return [
                "Chiến lược 80-89: xử lý đúng 2-3 khoảng trống lớn nhất để vượt 90, tránh sửa dàn trải.",
            ]
        elif final_score >= 70:
            return [
                "Chiến lược 70-79: tập trung 3 khoảng trống gây mất điểm lớn nhất thay vì thêm quá nhiều nội dung mới.",
            ]
        elif final_score >= 60:
            return [
                "Chiến lược 60-69: đồng thời tối ưu cấu trúc ATS và khoảng trống kỹ thuật để vượt ngưỡng vào danh sách rút gọn.",
            ]
        elif final_score >= 50:
            return [
                "Chiến lược 50-59: tái cấu trúc CV theo chuẩn ATS trước, rồi bổ sung kỹ năng nền tảng theo mức ưu tiên.",
            ]
        else:
            return [
                "Chiến lược <50: chọn JD gần năng lực hiện tại hơn và xây lộ trình nâng cấp kỹ năng theo 2 năng lực cốt lõi trước khi ứng tuyển lại.",
            ]


# Create singleton instance
_enhanced_scorer_instance = None

def get_enhanced_scorer() -> EnhancedCVScorer:
    """Get singleton instance of enhanced scorer"""
    global _enhanced_scorer_instance
    if _enhanced_scorer_instance is None:
        _enhanced_scorer_instance = EnhancedCVScorer()
    return _enhanced_scorer_instance
