"""
Final test to demonstrate enhanced scoring with keyword-specific feedback
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.enhanced_scoring import get_enhanced_scorer

def main():
    scorer = get_enhanced_scorer()
    
    # Vietnamese CV example
    cv_text_vi = """
    NGUYỄN VĂN MINH
    Senior Software Engineer
    Email: minh.nguyen@email.com | Phone: +84 912 345 678
    
    KINH NGHIỆM LÀM VIỆC:
    Senior Software Engineer - Tech Vietnam Co. (2020-2024) - 4 năm
    - Phát triển các REST API sử dụng Python và FastAPI, phục vụ 100K+ users
    - Xây dựng hệ thống microservices với Docker và Kubernetes trên AWS
    - Tối ưu hiệu năng database PostgreSQL, giảm thời gian query 50%
    - Dẫn dắt team 5 developers, áp dụng Agile/Scrum methodology
    - Triển khai CI/CD pipeline với Jenkins và GitHub Actions
    
    Software Developer - Startup ABC (2018-2020) - 2 năm
    - Phát triển ứng dụng web với React, Node.js và MongoDB
    - Cộng tác với team UX/UI để cải thiện user experience
    - Viết unit tests và integration tests với Jest và Pytest
    
    KỸ NĂNG:
    - Ngôn ngữ lập trình: Python, JavaScript, TypeScript
    - Frontend: React, Vue.js, HTML5, CSS3, Tailwind
    - Backend: FastAPI, Node.js, Express
    - Database: PostgreSQL, MySQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes
    - Tools: Git, Jenkins, GitHub Actions, Postman
    - Methodology: Agile, Scrum, REST API design
    
    HỌC VẤN:
    Cử nhân Khoa học Máy tính
    Đại học Bách Khoa, 2018
    
    THÀNH TỰU:
    - Cải thiện performance API lên 40%
    - Giảm deployment time từ 2 hours xuống 15 phút với CI/CD automation
    - Nhận giải thưởng "Best Technical Innovation" năm 2023
    
    NGÔN NGỮ:
    - Tiếng Việt: Bản ngữ
    - Tiếng Anh: Thành thạo (TOEIC 850)
    """
    
    # Job Description
    jd_text = """
    SENIOR BACKEND DEVELOPER
    
    YÊU CẦU:
    - 5+ năm kinh nghiệm phát triển phần mềm backend
    - Thành thạo Python, Java hoặc Go
    - Kinh nghiệm với React hoặc Angular
    - Kinh nghiệm thiết kế và phát triển microservices
    - Am hiểu PostgreSQL, MySQL và NoSQL databases (MongoDB, Cassandra)
    - Có kinh nghiệm với Docker và Kubernetes
    - Kinh nghiệm với Cloud platforms (AWS, GCP, hoặc Azure)
    - Kinh nghiệm với CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
    - Hiểu biết vững về RESTful APIs và GraphQL
    - Kinh nghiệm làm việc theo Agile/Scrum
    - Bằng cử nhân Khoa học Máy tính hoặc tương đương
    
    ƯU TIÊN:
    - Chứng chỉ AWS hoặc GCP
    - Kinh nghiệm với Terraform hoặc CloudFormation
    - Kinh nghiệm với GraphQL
    - Kinh nghiệm với message queues (Kafka, RabbitMQ)
    - Có kinh nghiệm leadership hoặc mentoring
    - Bằng thạc sĩ
    
    KỸ NĂNG MỀM:
    - Kỹ năng giải quyết vấn đề và phân tích tốt
    - Giao tiếp và làm việc nhóm xuất sắc
    - Kỹ năng leadership và mentoring
    - Chủ động và tự giác trong công việc
    """
    
    print("=" * 80)
    print("ENHANCED CV SCORING - VIETNAMESE EXAMPLE")
    print("=" * 80)
    
    result = scorer.score_cv(cv_text_vi, jd_text, "vi")
    
    print(f"\n📊 FINAL SCORE: {result['score']}/100")
    print("=" * 80)
    
    print("\n🔍 BREAKDOWN:")
    for component, score in result['breakdown'].items():
        bar_length = int(score / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"  {component.replace('_', ' ').title():20s} {bar} {score:5.1f}/100")
    
    print("\n" + "=" * 80)
    print("✅ STRENGTHS:")
    for i, strength in enumerate(result['strengths'], 1):
        print(f"  {i}. {strength}")
    
    print("\n" + "=" * 80)
    print("⚠️  WEAKNESSES (Missing from JD):")
    for i, weakness in enumerate(result['weaknesses'], 1):
        print(f"  {i}. {weakness}")
    
    print("\n" + "=" * 80)
    print("💡 IMPROVEMENT TIPS:")
    for i, tip in enumerate(result['improvement_tips'], 1):
        print(f"  {i}. {tip}")
    
    print("\n" + "=" * 80)
    print("🎯 KEYWORD MATCHING DETAILS:")
    
    print(f"\n  Technical Skills Matched ({len(result['matched_keywords']['technical'])}):")
    if result['matched_keywords']['technical']:
        tech_display = ', '.join(result['matched_keywords']['technical'][:15])
        if len(result['matched_keywords']['technical']) > 15:
            tech_display += f" + {len(result['matched_keywords']['technical']) - 15} more"
        print(f"    ✓ {tech_display}")
    else:
        print("    (none)")
    
    print(f"\n  Technical Skills Missing ({len(result['missing_keywords']['technical'])}):")
    if result['missing_keywords']['technical']:
        missing_tech = ', '.join(result['missing_keywords']['technical'][:10])
        if len(result['missing_keywords']['technical']) > 10:
            missing_tech += f" + {len(result['missing_keywords']['technical']) - 10} more"
        print(f"    ✗ {missing_tech}")
    else:
        print("    (none - excellent!)")
    
    print(f"\n  Soft Skills Matched ({len(result['matched_keywords']['soft_skills'])}):")
    if result['matched_keywords']['soft_skills']:
        print(f"    ✓ {', '.join(result['matched_keywords']['soft_skills'])}")
    else:
        print("    (none)")
    
    print(f"\n  Soft Skills Missing ({len(result['missing_keywords']['soft_skills'])}):")
    if result['missing_keywords']['soft_skills']:
        print(f"    ✗ {', '.join(result['missing_keywords']['soft_skills'])}")
    else:
        print("    (none - excellent!)")
    
    print(f"\n  Methodologies Matched ({len(result['matched_keywords']['methodologies'])}):")
    if result['matched_keywords']['methodologies']:
        print(f"    ✓ {', '.join(result['matched_keywords']['methodologies'])}")
    else:
        print("    (none)")
    
    print("\n" + "=" * 80)
    print("📈 METADATA:")
    meta = result['metadata']
    print(f"  CV Experience: {meta['cv_years']} years")
    print(f"  JD Required: {meta['jd_years']} years")
    print(f"  CV Education: {meta['cv_education']}")
    print(f"  JD Education: {meta['jd_education']}")
    print(f"  Detected Field: {meta['detected_field']}")
    
    if meta.get('inferred_soft_skills'):
        print(f"\n  Inferred Soft Skills from CV (context-based):")
        print(f"    → {', '.join(meta['inferred_soft_skills'])}")
    
    if meta.get('related_skill_matches'):
        print(f"\n  Related Skills (Partial Match):")
        for skill, score in meta['related_skill_matches'].items():
            print(f"    → {skill}: {score*100:.0f}% match")
    
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    
    if result['score'] >= 70:
        verdict = "STRONG CANDIDATE - Proceed to interview"
        emoji = "🌟"
    elif result['score'] >= 60:
        verdict = "GOOD CANDIDATE - Consider for interview"
        emoji = "👍"
    elif result['score'] >= 50:
        verdict = "AVERAGE CANDIDATE - Needs review"
        emoji = "📋"
    else:
        verdict = "WEAK MATCH - May not meet requirements"
        emoji = "⚠️"
    
    print(f"{emoji} {verdict}")
    print(f"\nThis CV matches {result['score']:.1f}% of the job requirements.")
    print(f"Main gaps: {', '.join(result['missing_keywords']['technical'][:5]) if result['missing_keywords']['technical'] else 'None'}")
    
    print("\n" + "=" * 80)
    
    return result

if __name__ == "__main__":
    main()
