"""
Quick test script to verify advanced scoring algorithm
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.advanced_scoring import get_advanced_scorer

def test_advanced_scoring():
    scorer = get_advanced_scorer()
    
    # Sample CV text
    cv_text = """
    NGUYEN VAN A
    Senior Software Engineer
    
    EXPERIENCE:
    Software Developer at ABC Company (2019-2024) - 5 years
    - Developed REST APIs using Python, FastAPI, and PostgreSQL
    - Built microservices with Docker and Kubernetes
    - Implemented CI/CD pipelines with GitHub Actions
    - Led team of 3 developers in agile environment
    
    SKILLS:
    Programming: Python, JavaScript, TypeScript, Java
    Frontend: React, Vue.js, HTML, CSS
    Backend: Node.js, Express, FastAPI, Django
    Database: PostgreSQL, MySQL, MongoDB, Redis
    Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
    Tools: Git, Jenkins, GitHub Actions
    
    EDUCATION:
    Bachelor of Computer Science
    University of Technology, 2019
    
    ACHIEVEMENTS:
    - Improved API performance by 40%
    - Reduced deployment time by 60% with CI/CD
    - AWS Certified Solutions Architect
    
    LANGUAGES:
    - English: Fluent
    - Vietnamese: Native
    """
    
    # Sample JD text
    jd_text = """
    SENIOR SOFTWARE ENGINEER
    
    REQUIREMENTS:
    - 5+ years of experience in software development
    - Strong proficiency in Python, JavaScript/TypeScript
    - Experience with React or Vue.js
    - Experience with microservices architecture
    - Proficiency in PostgreSQL and NoSQL databases (MongoDB, Redis)
    - Hands-on experience with Docker and Kubernetes
    - Cloud platform experience (AWS, GCP, or Azure)
    - Experience with CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI)
    - Solid understanding of RESTful APIs and GraphQL
    - Agile/Scrum methodology experience
    - Bachelor's degree in Computer Science or related field
    
    PREFERRED:
    - AWS or GCP certifications
    - Experience with Terraform or CloudFormation
    - Knowledge of GraphQL
    - Experience with message queues (Kafka, RabbitMQ)
    - Leadership or mentoring experience
    - Master's degree
    
    SOFT SKILLS:
    - Strong problem-solving and analytical skills
    - Excellent communication and teamwork
    - Leadership and mentoring abilities
    - Self-motivated and proactive
    """
    
    print("Testing Advanced Scoring Algorithm...")
    print("=" * 60)
    
    result = scorer.score_cv(cv_text, jd_text, "en")
    
    print(f"\nFINAL SCORE: {result['score']}/100")
    print("=" * 60)
    
    print("\nBREAKDOWN:")
    for component, score in result['breakdown'].items():
        print(f"  {component.replace('_', ' ').title()}: {score:.2f}")
    
    print("\n" + "=" * 60)
    print("STRENGTHS:")
    for i, strength in enumerate(result['strengths'], 1):
        print(f"  {i}. {strength}")
    
    print("\n" + "=" * 60)
    print("WEAKNESSES:")
    for i, weakness in enumerate(result['weaknesses'], 1):
        print(f"  {i}. {weakness}")
    
    print("\n" + "=" * 60)
    print("IMPROVEMENT TIPS:")
    for i, tip in enumerate(result['improvement_tips'], 1):
        print(f"  {i}. {tip}")
    
    print("\n" + "=" * 60)
    print("MATCHED KEYWORDS:")
    print(f"  Technical ({len(result['matched_keywords']['technical'])}): {', '.join(result['matched_keywords']['technical'][:15])}")
    if len(result['matched_keywords']['technical']) > 15:
        print(f"    + {len(result['matched_keywords']['technical']) - 15} more...")
    print(f"  Soft Skills ({len(result['matched_keywords']['soft_skills'])}): {', '.join(result['matched_keywords']['soft_skills'])}")
    print(f"  Methodologies ({len(result['matched_keywords']['methodologies'])}): {', '.join(result['matched_keywords']['methodologies'])}")
    
    print("\n" + "=" * 60)
    print("MISSING KEYWORDS:")
    print(f"  Technical ({len(result['missing_keywords']['technical'])}): {', '.join(result['missing_keywords']['technical'][:10])}")
    if len(result['missing_keywords']['technical']) > 10:
        print(f"    + {len(result['missing_keywords']['technical']) - 10} more...")
    print(f"  Soft Skills ({len(result['missing_keywords']['soft_skills'])}): {', '.join(result['missing_keywords']['soft_skills'])}")
    print(f"  Methodologies ({len(result['missing_keywords']['methodologies'])}): {', '.join(result['missing_keywords']['methodologies'])}")
    
    print("\n" + "=" * 60)
    print("METADATA:")
    print(f"  CV Experience: {result['metadata']['cv_years']} years")
    print(f"  JD Required: {result['metadata']['jd_years']} years")
    print(f"  CV Education: {result['metadata']['cv_education']}")
    print(f"  JD Education: {result['metadata']['jd_education']}")
    print(f"  CV Certifications: {', '.join(result['metadata']['cv_certifications']) if result['metadata']['cv_certifications'] else 'None'}")
    print(f"  CV Sections: {', '.join([k for k, v in result['metadata']['cv_sections'].items() if v])}")
    
    print("\n" + "=" * 60)
    print("\nTest completed successfully!")
    
    # Verify score is better than old algorithm
    if result['score'] >= 70:
        print(f"✓ Score {result['score']} >= 70 - EXCELLENT MATCH")
    elif result['score'] >= 60:
        print(f"✓ Score {result['score']} >= 60 - GOOD MATCH")
    else:
        print(f"! Score {result['score']} < 60 - Needs improvement")
    
    return result

if __name__ == "__main__":
    test_advanced_scoring()
