"""
Test script to demonstrate improved CV scoring feedback
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.enhanced_scoring import get_enhanced_scorer

def print_section(title, items, emoji="•"):
    """Pretty print a feedback section"""
    print(f"\n{title}")
    print("=" * 80)
    for i, item in enumerate(items, 1):
        print(f"{emoji} {item}")

def test_low_score_feedback():
    """Test feedback for low-scoring CV (40/100)"""
    print("\n" + "=" * 80)
    print("TEST CASE 1: LOW SCORE CV (Missing many skills)")
    print("=" * 80)
    
    cv_text = """
    Nguyễn Văn A
    Software Developer
    
    Kinh nghiệm: 2 năm
    
    - Làm việc với HTML, CSS
    - Biết chút JavaScript
    - Đã làm vài dự án web nhỏ
    
    Học vấn: Đại học Bách Khoa
    """
    
    jd_text = """
    Senior Full Stack Developer (5+ years experience)
    
    Required skills:
    - React, Node.js, TypeScript
    - PostgreSQL, MongoDB
    - Docker, Kubernetes
    - AWS, CI/CD
    - Agile, Scrum
    
    Soft skills:
    - Leadership, Team management
    - Communication, Problem solving
    """
    
    scorer = get_enhanced_scorer()
    result = scorer.score_cv(cv_text, jd_text, language="vi", field="software")
    
    print(f"\n📊 SCORE: {result['score']:.1f}/100")
    print_section("✅ ĐIỂM MẠNH:", result['strengths'], "✓")
    print_section("⚠️  ĐIỂM YẾU:", result['weaknesses'], "✗")
    print_section("💡 LỜI KHUYÊN:", result['improvement_tips'], "→")


def test_medium_score_feedback():
    """Test feedback for medium-scoring CV (65/100)"""
    print("\n\n" + "=" * 80)
    print("TEST CASE 2: MEDIUM SCORE CV (Has foundation but missing some skills)")
    print("=" * 80)
    
    cv_text = """
    John Doe - Full Stack Developer
    
    Experience: 4 years in web development
    
    Technical Skills:
    - Frontend: React, HTML, CSS, JavaScript
    - Backend: Node.js, Express
    - Database: MySQL, MongoDB
    - Tools: Git, VS Code
    
    Work Experience:
    - Built e-commerce platform with React and Node.js
    - Managed database with 100k+ records
    - Worked in agile team of 5 developers
    - Improved page load time by 40%
    
    Education: Computer Science, State University
    """
    
    jd_text = """
    Senior Full Stack Developer (4+ years)
    
    Must have:
    - React, TypeScript, Node.js
    - PostgreSQL or MySQL
    - Docker, AWS
    - Git, CI/CD pipelines
    
    Soft skills:
    - Team leadership
    - Problem solving
    - Communication
    """
    
    scorer = get_enhanced_scorer()
    result = scorer.score_cv(cv_text, jd_text, language="vi", field="software")
    
    print(f"\n📊 SCORE: {result['score']:.1f}/100")
    print_section("✅ ĐIỂM MẠNH:", result['strengths'], "✓")
    print_section("⚠️  ĐIỂM YẾU:", result['weaknesses'], "✗")
    print_section("💡 LỜI KHUYÊN:", result['improvement_tips'], "→")


def test_high_score_feedback():
    """Test feedback for high-scoring CV (85/100)"""
    print("\n\n" + "=" * 80)
    print("TEST CASE 3: HIGH SCORE CV (Well-matched with minor gaps)")
    print("=" * 80)
    
    cv_text = """
    Jane Smith - Senior Full Stack Engineer
    
    Professional Summary:
    5+ years of experience building scalable web applications using React, TypeScript, Node.js.
    Proven track record in AWS cloud infrastructure and Docker containerization.
    Strong leadership and team collaboration skills.
    
    Technical Skills:
    - Frontend: React, TypeScript, JavaScript, Redux, HTML5, CSS3
    - Backend: Node.js, Express, NestJS, Python
    - Database: PostgreSQL, MongoDB, Redis
    - Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Jenkins, CI/CD
    - Methodologies: Agile, Scrum, Test-Driven Development
    
    Experience:
    Senior Developer at TechCorp (3 years)
    - Led team of 6 developers in building microservices architecture
    - Reduced deployment time by 60% through CI/CD automation
    - Architected scalable system handling 1M+ daily active users
    - Mentored 4 junior developers, improving team velocity by 35%
    
    Mid-level Developer at StartupXYZ (2 years)
    - Built React-based dashboard increasing user engagement by 45%
    - Optimized database queries reducing response time from 2s to 200ms
    - Implemented Docker containers improving development efficiency
    
    Education:
    B.S. Computer Science, Tech University (GPA: 3.8/4.0)
    
    Certifications:
    - AWS Certified Solutions Architect
    """
    
    jd_text = """
    Senior Full Stack Engineer (5+ years)
    
    Required:
    - React, TypeScript, Node.js
    - PostgreSQL, MongoDB
    - AWS, Docker, Kubernetes
    - CI/CD, Jenkins or GitHub Actions
    - Agile, Scrum
    
    Preferred:
    - Team leadership experience
    - Microservices architecture
    - Performance optimization
    
    Soft Skills:
    - Leadership
    - Communication
    - Problem solving
    - Mentoring
    """
    
    scorer = get_enhanced_scorer()
    result = scorer.score_cv(cv_text, jd_text, language="vi", field="software")
    
    print(f"\n📊 SCORE: {result['score']:.1f}/100")
    print_section("✅ ĐIỂM MẠNH:", result['strengths'], "✓")
    print_section("⚠️  ĐIỂM YẾU:", result['weaknesses'], "✗")
    print_section("💡 LỜI KHUYÊN:", result['improvement_tips'], "→")


def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    IMPROVED CV FEEDBACK SYSTEM - DEMO                      ║
║                                                                            ║
║  This demonstrates the enhanced feedback with:                            ║
║  ✓ Clear, specific strengths highlighting what CV does well              ║
║  ✓ Actionable weaknesses explaining gaps and their impact                ║
║  ✓ Detailed, step-by-step tips for improvement                           ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    test_low_score_feedback()
    test_medium_score_feedback()
    test_high_score_feedback()
    
    print("\n" + "=" * 80)
    print("SUMMARY OF IMPROVEMENTS:")
    print("=" * 80)
    print("""
OLD FEEDBACK:
  Strengths: "CV contains relevant signals but needs clearer alignment with JD."
  Weaknesses: "CV misses some standard sections (experience/skills/education/projects)."
  Tips: "Add missing CV sections to improve recruiter readability and ATS matching."

NEW FEEDBACK:
  Strengths: Specific skills matched with counts and context
  Weaknesses: Clear explanation of what's missing and WHY it matters
  Tips: Step-by-step action plan with priority levels and examples

KEY FEATURES:
  ✓ Score-based contextual feedback (90+, 80+, 70+, 60+, <50)
  ✓ Quantified metrics (X/Y skills matched, % match rate)
  ✓ Emoji indicators for quick scanning
  ✓ Priority levels (ƯTIÊN CAO, BƯỚC 2)
  ✓ Field-specific tips (software vs marketing vs HR)
  ✓ ATS optimization guidance
  ✓ Concrete examples and formulas
    """)


if __name__ == "__main__":
    main()
