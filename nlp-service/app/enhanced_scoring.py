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
        """Generate detailed, actionable feedback with clear strengths, weaknesses and tips."""

        strengths: List[str] = []
        weaknesses: List[str] = []
        tips: List[str] = []

        matched_tech_count = len(matched_tech)
        total_tech_required = matched_tech_count + len(missing_tech)
        matched_soft_count = len(matched_soft)
        total_soft_required = matched_soft_count + len(missing_soft)
        
        tech_match_rate = (matched_tech_count / total_tech_required * 100) if total_tech_required > 0 else 0
        soft_match_rate = (matched_soft_count / total_soft_required * 100) if total_soft_required > 0 else 0

        # ============= STRENGTHS =============
        # 1. Overall assessment
        strengths.append(self._score_band_summary(final_score, language))

        # 2. Technical skills strengths
        if matched_tech_count > 0:
            if tech_match_rate >= 70:
                matched_list = ', '.join(sorted(list(matched_tech))[:5])
                strengths.append(
                    f"Kỹ năng kỹ thuật xuất sắc ({matched_tech_count}/{total_tech_required}): CV thể hiện rõ {matched_list}"
                    + (f" và {matched_tech_count - 5} kỹ năng khác" if matched_tech_count > 5 else "")
                )
            elif tech_match_rate >= 40:
                matched_list = ', '.join(sorted(list(matched_tech))[:4])
                strengths.append(
                    f"Có nền tảng kỹ thuật phù hợp ({matched_tech_count}/{total_tech_required}): Đã match {matched_list}"
                )
            else:
                matched_list = ', '.join(sorted(list(matched_tech))[:3])
                strengths.append(f"Có một số kỹ năng liên quan: {matched_list}")

        # 3. Soft skills and inferred skills
        if matched_soft_count > 0 or inferred_soft:
            soft_skills_total = matched_soft_count + len(inferred_soft)
            if soft_skills_total >= 3:
                combined_soft = list(matched_soft)[:3] + list(inferred_soft)[:2]
                strengths.append(
                    f"Thể hiện tốt kỹ năng mềm ({soft_skills_total} kỹ năng): {', '.join(sorted(combined_soft[:5]))}"
                )
            elif matched_soft_count > 0:
                strengths.append(f"Có đề cập kỹ năng mềm: {', '.join(sorted(list(matched_soft))[:3])}")

        # 4. Experience alignment
        if jd_years > 0:
            if cv_years >= jd_years:
                years_excess = cv_years - jd_years
                if years_excess >= 2:
                    strengths.append(
                        f"Kinh nghiệm vượt yêu cầu: {cv_years} năm (vượt {years_excess} năm so với JD)"
                    )
                else:
                    strengths.append(f"Kinh nghiệm đáp ứng yêu cầu: {cv_years} năm (JD yêu cầu {jd_years} năm)")
            elif cv_years >= jd_years * 0.7:
                strengths.append(f"Kinh nghiệm gần đạt yêu cầu: {cv_years} năm (JD yêu cầu {jd_years} năm)")

        # 5. Related/transferable skills
        related_matches = {k: v for k, v in tech_matches.items() if 0.3 < v < 1.0}
        if related_matches and len(related_matches) >= 2:
            related_list = ', '.join(list(sorted(related_matches.keys()))[:4])
            strengths.append(
                f"Có kỹ năng liên quan đáng giá ({len(related_matches)} kỹ năng): {related_list}"
            )

        # 6. Structure completeness
        present_sections = [k for k, v in sections.items() if v]
        if len(present_sections) >= 3:
            strengths.append(f"Cấu trúc CV đầy đủ với {len(present_sections)} mục chính: {', '.join(present_sections[:4])}")

        # ============= WEAKNESSES =============
        # 1. Critical missing technical skills
        if missing_tech:
            critical_missing = sorted(list(missing_tech))[:5]
            if len(missing_tech) >= 5:
                weaknesses.append(
                    f"Thiếu nhiều kỹ năng kỹ thuật quan trọng ({len(missing_tech)} kỹ năng): {', '.join(critical_missing)} - Đây là rào cản lớn với ATS và nhà tuyển dụng"
                )
            elif len(missing_tech) >= 3:
                weaknesses.append(
                    f"Thiếu một số kỹ năng kỹ thuật cốt lõi ({len(missing_tech)} kỹ năng): {', '.join(critical_missing)} - Cần bổ sung để tăng cơ hội"
                )
            else:
                weaknesses.append(
                    f"Chưa thể hiện rõ: {', '.join(critical_missing)} - Đây là kỹ năng JD yêu cầu"
                )

        # 2. Missing soft skills
        if missing_soft:
            soft_missing = sorted(list(missing_soft))[:4]
            if len(missing_soft) >= 4:
                weaknesses.append(
                    f"Thiếu kỹ năng mềm ({len(missing_soft)} kỹ năng): {', '.join(soft_missing)} - Cần viết lại bullet points để thể hiện"
                )
            else:
                weaknesses.append(f"Chưa nhấn mạnh kỹ năng mềm: {', '.join(soft_missing)}")

        # 3. Experience gap
        if jd_years > 0 and cv_years < jd_years * 0.7:
            gap = jd_years - cv_years
            weaknesses.append(
                f"Kinh nghiệm chưa đạt yêu cầu: CV {cv_years} năm, JD yêu cầu {jd_years} năm (thiếu {gap:.1f} năm) - Cần bù bằng kỹ năng hoặc dự án nổi bật"
            )

        # 4. Missing methodologies
        if missing_method:
            method_missing = sorted(list(missing_method))[:4]
            weaknesses.append(
                f"Thiếu phương pháp làm việc: {', '.join(method_missing)} - Đây là yếu tố quan trọng để đánh giá quy trình làm việc"
            )

        # 5. Weak component breakdown
        weakest_components = sorted(breakdown_scores.items(), key=lambda x: x[1])[:2]
        for comp, comp_score in weakest_components:
            if comp_score < 40:
                comp_label = self._component_label(comp)
                weaknesses.append(
                    f"Phần {comp_label} rất yếu ({comp_score:.1f}/100): Cần cải thiện đáng kể để vượt vòng sơ tuyển"
                )

        # 6. Structure issues
        missing_sections = [k for k, v in sections.items() if not v]
        if missing_sections:
            if len(missing_sections) >= 3:
                weaknesses.append(
                    f"Thiếu {len(missing_sections)} mục quan trọng: {', '.join(missing_sections[:4])} - ATS thường tìm các mục này để parse dữ liệu"
                )
            else:
                weaknesses.append(f"Thiếu mục CV: {', '.join(missing_sections)} - Nên bổ sung để tăng tính chuyên nghiệp")

        # ============= TIPS =============
        # 1. Score-based strategic tips
        tips.extend(self._score_band_tips(final_score, language))

        # 2. Technical skills action plan
        if missing_tech:
            priority_tech = sorted(list(missing_tech))[:3]
            if len(missing_tech) <= 3:
                tips.append(
                    f"ƯU TIÊN CAO: Bổ sung ngay {', '.join(priority_tech)} vào CV - Thêm 1-2 dự án cụ thể cho mỗi kỹ năng này"
                )
            else:
                tips.append(
                    f"ƯU TIÊN CAO: Tập trung vào top 3 kỹ năng thiếu ({', '.join(priority_tech)}) - Viết 2-3 bullet points với kết quả đo lường được cho mỗi kỹ năng"
                )
                
            # Add second-tier tech tips
            if len(missing_tech) > 3:
                secondary_tech = sorted(list(missing_tech))[3:6]
                tips.append(
                    f"BƯỚC 2: Sau khi bổ sung top 3, hãy thêm: {', '.join(secondary_tech)} để tăng độ phủ lên 80%+"
                )

        # 3. Soft skills enhancement
        if missing_soft or (matched_soft_count > 0 and matched_soft_count < total_soft_required):
            if missing_soft:
                priority_soft = sorted(list(missing_soft))[:2]
                tips.append(
                    f"Viết lại experience bullets để thể hiện {', '.join(priority_soft)} - Dùng công thức: [Hành động] + [Kết quả] + [Tác động]"
                )
            if matched_soft_count > 0:
                tips.append(
                    "Soft skills đã có cần được NHẤN MẠNH hơn: Đưa lên phần tóm tắt hoặc top 3 bullets của mỗi công việc"
                )

        # 4. Experience gap solutions
        if jd_years > 0 and cv_years < jd_years:
            gap = jd_years - cv_years
            if gap >= 2:
                tips.append(
                    f"Bù đắp khoảng trống {gap:.0f} năm kinh nghiệm: (1) Nhấn mạnh độ phức tạp/quy mô dự án, (2) Thêm freelance/side projects, (3) Highlight leadership hoặc impact lớn"
                )
            else:
                tips.append(
                    "Tối ưu phần kinh nghiệm: Thêm metrics cụ thể (tăng trưởng %, số lượng users, revenue...) để thể hiện impact tương đương senior"
                )

        # 5. ATS optimization
        if final_score < 60:
            tips.append(
                "Tối ưu ATS: (1) Sao chép CHÍNH XÁC từ khóa từ JD, (2) Đưa từ khóa quan trọng lên đầu mỗi section, (3) Tránh table/hình ảnh trong phần skills"
            )

        # 6. Field-specific tips
        if field == "software":
            if missing_tech and breakdown_scores.get("technical_skills", 0) < 50:
                tips.append(
                    "Chiến lược cho Software role: Tạo GitHub repo demo các tech thiếu + link vào CV, hoặc viết blog post về cách implement"
                )
        elif field in ["marketing", "hr"] and soft_match_rate < 50:
            tips.append(
                "Chiến lược cho Marketing/HR role: Mỗi bullet point cần có số liệu cụ thể (conversion rate, engagement, retention...) để thể hiện soft skills"
            )

        # 7. Structure improvements
        if missing_sections:
            section_tips = {
                "experience": "Thêm mục KINH NGHIỆM với format: [Vị trí] | [Công ty] | [Thời gian] - Liệt kê 3-5 achievements",
                "education": "Thêm mục HỌC VẤN: Tên trường, chuyên ngành, năm tốt nghiệp (GPA nếu >= 3.0/4.0)",
                "skills": "Thêm mục KỸ NĂNG: Phân loại theo nhóm (Technical, Soft Skills, Languages) với cấp độ thành thạo",
                "projects": "Thêm mục DỰ ÁN: 2-3 projects nổi bật với tech stack, role và kết quả đạt được",
            }
            for missing_sec in missing_sections[:2]:
                if missing_sec in section_tips:
                    tips.append(section_tips[missing_sec])

        # Fallback guards
        if not strengths:
            strengths.append("CV có một số tín hiệu phù hợp nhưng cần điều chỉnh để tăng độ match với JD này")
        
        if not weaknesses:
            weaknesses.append("Không phát hiện điểm yếu nghiêm trọng - Chỉ cần tối ưu nhỏ để đạt điểm cao hơn")

        if len(tips) < 3:
            tips.append("Sử dụng từ khóa chính xác từ JD trong phần tóm tắt và top 3 bullet points")
            tips.append("Thêm số liệu định lượng (%, số lượng, thời gian) vào mọi achievement có thể")

        return {
            "strengths": strengths[:8],
            "weaknesses": weaknesses[:8],
            "tips": tips[:10]
        }

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

    def _score_band_summary(
        self,
        final_score: float,
        language: str,
    ) -> str:
        """Generate detailed score band summary with actionable context"""
        _ = str(language).lower()
        if final_score >= 90:
            return f"✨ PHÙ HỢP XUẤT SẮC ({final_score:.1f}/100): CV match hầu hết yêu cầu JD - Rất có khả năng vượt vòng sơ tuyển ATS"
        elif final_score >= 80:
            return f"⭐ PHÙ HỢP CAO ({final_score:.1f}/100): CV khớp tốt với JD - Có cơ hội cao được mời phỏng vấn nếu tối ưu thêm một số điểm"
        elif final_score >= 70:
            return f"✓ PHÙ HỢP KHÁ ({final_score:.1f}/100): CV có nền tảng tốt - Cần bổ sung một số kỹ năng quan trọng để tăng cạnh tranh"
        elif final_score >= 60:
            return f"△ PHÙ HỢP TRUNG BÌNH ({final_score:.1f}/100): CV đáp ứng một phần yêu cầu - Cần cải thiện đáng kể để có cơ hội"
        elif final_score >= 50:
            return f"⚠ PHÙ HỢP THẤP ({final_score:.1f}/100): CV còn thiếu nhiều yêu cầu cốt lõi - Nguy cơ cao bị loại bởi ATS"
        else:
            return f"✗ PHÙ HỢP RẤT THẤP ({final_score:.1f}/100): CV chưa match với JD này - Nên xem xét apply vị trí khác hoặc học thêm kỹ năng"

    def _score_band_tips(self, final_score: float, language: str) -> List[str]:
        """Generate strategic tips based on score band"""
        _ = str(language).lower()
        if final_score >= 90:
            return [
                "🎯 CHIẾN LƯỢC ĐẠT 95+: Thêm 1-2 certifications liên quan hoặc side projects để vượt trội hoàn toàn",
                "📝 POLISH CV: Đảm bảo không có lỗi grammar, format nhất quán, và tailored cho từng company culture",
            ]
        elif final_score >= 80:
            return [
                "🎯 CHIẾN LƯỢC ĐẠT 90+: Điền đầy kỹ năng thiếu và thêm 2-3 achievements với metrics cụ thể",
                "📊 QUANTIFY RESULTS: Mỗi bullet point nên có con số (%, $, time saved, users impacted...)",
            ]
        elif final_score >= 70:
            return [
                "🎯 CHIẾN LƯỢC ĐẠT 80+: Tập trung vào top 3-5 kỹ năng thiếu quan trọng nhất, viết case study cho mỗi skill",
                "🔑 KEYWORDS: Scan JD tìm từ khóa xuất hiện 2+ lần, đảm bảo chúng có trong CV (chính xác 100%)",
            ]
        elif final_score >= 60:
            return [
                "🎯 CHIẾN LƯỢC ĐẠT 70+: Bổ sung ngay top 5 kỹ năng thiếu + viết lại summary để mirror JD requirements",
                "⚡ QUICK WINS: (1) Copy exact job title từ JD, (2) Thêm years of experience rõ ràng, (3) Đảm bảo có các section chuẩn",
            ]
        elif final_score >= 50:
            return [
                "🎯 CHIẾN LƯỢC ĐẠT 60+: Học/bổ sung 5-7 kỹ năng thiếu qua online courses (Udemy, Coursera) hoặc mini projects",
                "🔧 RESTRUCTURE: Viết lại CV theo format ATS-friendly: [Summary] > [Skills] > [Experience] > [Education]",
            ]
        else:
            return [
                "🎯 XEM XÉT LẠI: CV này có thể không phù hợp với JD - Cân nhắc apply những vị trí match hơn với skillset hiện tại",
                "📚 UPSKILL: JD này yêu cầu nhiều skills chưa có - Nên đầu tư 2-3 tháng học hoặc tìm junior position trước",
            ]


# Create singleton instance
_enhanced_scorer_instance = None

def get_enhanced_scorer() -> EnhancedCVScorer:
    """Get singleton instance of enhanced scorer"""
    global _enhanced_scorer_instance
    if _enhanced_scorer_instance is None:
        _enhanced_scorer_instance = EnhancedCVScorer()
    return _enhanced_scorer_instance
