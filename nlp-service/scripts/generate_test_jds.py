"""
Generate test Job Descriptions for CV scoring evaluation
"""
import json
from pathlib import Path
from typing import Dict, List

JD_TEMPLATES = {
    "software": {
        "vi": """VỊ TRÍ: {title}

MÔ TẢ CÔNG VIỆC:
- Phát triển và bảo trì các ứng dụng {tech_stack}
- Thiết kế và triển khai API RESTful
- Làm việc với cơ sở dữ liệu {database}
- Tham gia code review và đảm bảo chất lượng code
- Làm việc theo phương pháp Agile/Scrum
- Tối ưu hóa hiệu suất ứng dụng

YÊU CẦU:
- Tối thiểu {exp_years} năm kinh nghiệm làm việc với {key_skills}
- Thành thạo {programming_languages}
- Kinh nghiệm với {framework}
- Hiểu biết về Git, CI/CD
- Kỹ năng làm việc nhóm tốt
- Tiếng Anh giao tiếp

ƯU TIÊN:
- Kinh nghiệm với {bonus_skills}
- Đã từng tham gia dự án lớn
- Có khả năng mentoring junior developers
""",
        "en": """POSITION: {title}

JOB DESCRIPTION:
- Develop and maintain {tech_stack} applications
- Design and implement RESTful APIs
- Work with {database} databases
- Participate in code reviews and ensure code quality
- Work in Agile/Scrum environment
- Optimize application performance

REQUIREMENTS:
- Minimum {exp_years} years of experience with {key_skills}
- Proficient in {programming_languages}
- Experience with {framework}
- Knowledge of Git, CI/CD
- Strong teamwork skills
- Good English communication

PREFERRED:
- Experience with {bonus_skills}
- Previously worked on large-scale projects
- Ability to mentor junior developers
"""
    },
    "data": {
        "vi": """VỊ TRÍ: {title}

MÔ TẢ CÔNG VIỆC:
- Phân tích dữ liệu và xây dựng mô hình dự đoán
- Làm sạch và xử lý dữ liệu lớn
- Tạo dashboard và báo cáo trực quan
- Làm việc với {tools} để phân tích dữ liệu
- Triển khai mô hình {ml_type}
- Cộng tác với các team khác để hiểu business requirements

YÊU CẦU:
- Tối thiểu {exp_years} năm kinh nghiệm phân tích dữ liệu
- Thành thạo {programming_languages}
- Kinh nghiệm với {key_skills}
- Hiểu biết về thống kê và xác suất
- SQL và database queries
- Kỹ năng trình bày và communication

ƯU TIÊN:
- Kinh nghiệm với {bonus_skills}
- Kinh nghiệm triển khai mô hình vào production
- Background về toán hoặc thống kê
""",
        "en": """POSITION: {title}

JOB DESCRIPTION:
- Analyze data and build predictive models
- Clean and process large datasets
- Create dashboards and visual reports
- Work with {tools} for data analysis
- Deploy {ml_type} models
- Collaborate with teams to understand business requirements

REQUIREMENTS:
- Minimum {exp_years} years of data analysis experience
- Proficient in {programming_languages}
- Experience with {key_skills}
- Understanding of statistics and probability
- SQL and database queries
- Strong presentation and communication skills

PREFERRED:
- Experience with {bonus_skills}
- Experience deploying models to production
- Background in mathematics or statistics
"""
    },
    "marketing": {
        "vi": """VỊ TRÍ: {title}

MÔ TẢ CÔNG VIỆC:
- Lập kế hoạch và thực hiện chiến dịch marketing
- Quản lý {channels} channels
- Phân tích hiệu quả chiến dịch và tối ưu ROI
- Tạo nội dung sáng tạo cho các kênh marketing
- Làm việc với {tools} để quản lý campaigns
- Nghiên cứu thị trường và đối thủ cạnh tranh

YÊU CẦU:
- Tối thiểu {exp_years} năm kinh nghiệm marketing
- Thành thạo {key_skills}
- Kinh nghiệm với Google Analytics, Facebook Ads
- Kỹ năng sáng tạo nội dung
- Hiểu biết về SEO/SEM
- Kỹ năng phân tích và báo cáo

ƯU TIÊN:
- Kinh nghiệm với {bonus_skills}
- Đã quản lý ngân sách marketing lớn
- Kỹ năng design cơ bản (Photoshop, Canva)
""",
        "en": """POSITION: {title}

JOB DESCRIPTION:
- Plan and execute marketing campaigns
- Manage {channels} channels
- Analyze campaign performance and optimize ROI
- Create creative content for marketing channels
- Work with {tools} for campaign management
- Research market and competitors

REQUIREMENTS:
- Minimum {exp_years} years of marketing experience
- Proficient in {key_skills}
- Experience with Google Analytics, Facebook Ads
- Strong content creation skills
- Understanding of SEO/SEM
- Analytical and reporting skills

PREFERRED:
- Experience with {bonus_skills}
- Managed large marketing budgets
- Basic design skills (Photoshop, Canva)
"""
    },
    "finance": {
        "vi": """VỊ TRÍ: {title}

MÔ TẢ CÔNG VIỆC:
- Phân tích báo cáo tài chính và lập ngân sách
- Thực hiện {tasks} hàng tháng/quý/năm
- Làm việc với {tools} để quản lý tài chính
- Đảm bảo tuân thủ các quy định kế toán
- Phối hợp với các phòng ban khác
- Chuẩn bị báo cáo cho ban lãnh đạo

YÊU CẦU:
- Tối thiểu {exp_years} năm kinh nghiệm {field}
- Thành thạo {key_skills}
- Hiểu biết về VAS, IFRS
- Thành thạo Excel, ERP systems
- Tỉ mỉ, cẩn thận trong công việc
- Kỹ năng phân tích tốt

ƯU TIÊN:
- Chứng chỉ {bonus_skills}
- Kinh nghiệm audit
- Kinh nghiệm ngành {industry}
""",
        "en": """POSITION: {title}

JOB DESCRIPTION:
- Analyze financial reports and create budgets
- Perform {tasks} monthly/quarterly/annually
- Work with {tools} for financial management
- Ensure compliance with accounting regulations
- Coordinate with other departments
- Prepare reports for management

REQUIREMENTS:
- Minimum {exp_years} years of {field} experience
- Proficient in {key_skills}
- Understanding of GAAP, IFRS
- Proficient in Excel, ERP systems
- Detail-oriented and careful
- Strong analytical skills

PREFERRED:
- Certifications in {bonus_skills}
- Audit experience
- Industry experience in {industry}
"""
    },
    "hr": {
        "vi": """VỊ TRÍ: {title}

MÔ TẢ CÔNG VIỆC:
- Quản lý quy trình tuyển dụng end-to-end
- Xây dựng và duy trì văn hóa doanh nghiệp
- Thực hiện {tasks}
- Làm việc với {tools} để quản lý nhân sự
- Tư vấn cho managers về các vấn đề nhân sự
- Tổ chức training và development programs

YÊU CẦU:
- Tối thiểu {exp_years} năm kinh nghiệm HR
- Thành thạo {key_skills}
- Hiểu biết về luật lao động Việt Nam
- Kinh nghiệm với HRIS systems
- Kỹ năng giao tiếp và đàm phán tốt
- Kỹ năng giải quyết xung đột

ƯU TIÊN:
- Kinh nghiệm {bonus_skills}
- Đã từng làm trong môi trường đa quốc gia
- Chứng chỉ HR professional
""",
        "en": """POSITION: {title}

JOB DESCRIPTION:
- Manage end-to-end recruitment process
- Build and maintain company culture
- Perform {tasks}
- Work with {tools} for HR management
- Advise managers on HR issues
- Organize training and development programs

REQUIREMENTS:
- Minimum {exp_years} years of HR experience
- Proficient in {key_skills}
- Understanding of labor laws
- Experience with HRIS systems
- Strong communication and negotiation skills
- Conflict resolution skills

PREFERRED:
- Experience in {bonus_skills}
- Worked in multinational environment
- HR professional certification
"""
    }
}

JD_VARIATIONS = {
    "software": [
        {
            "title": "Senior Backend Developer",
            "tech_stack": "microservices và cloud-native",
            "database": "PostgreSQL, MongoDB, Redis",
            "key_skills": "Python, Java, hoặc Go",
            "programming_languages": "Python/Java/Go",
            "framework": "FastAPI, Spring Boot, hoặc Gin",
            "bonus_skills": "Kubernetes, Docker, AWS",
            "exp_years": 5
        },
        {
            "title": "Full-stack Developer",
            "tech_stack": "web applications",
            "database": "MySQL, PostgreSQL",
            "key_skills": "JavaScript, React, Node.js",
            "programming_languages": "JavaScript/TypeScript",
            "framework": "React, Vue.js, hoặc Angular",
            "bonus_skills": "Next.js, GraphQL, Docker",
            "exp_years": 3
        },
        {
            "title": "DevOps Engineer",
            "tech_stack": "CI/CD pipelines và infrastructure",
            "database": "MySQL, PostgreSQL, MongoDB",
            "key_skills": "Docker, Kubernetes, AWS/GCP",
            "programming_languages": "Python, Bash, Go",
            "framework": "Terraform, Ansible, Jenkins",
            "bonus_skills": "Prometheus, Grafana, ELK Stack",
            "exp_years": 4
        }
    ],
    "data": [
        {
            "title": "Senior Data Scientist",
            "tools": "Python, TensorFlow, PyTorch",
            "ml_type": "Machine Learning và Deep Learning",
            "programming_languages": "Python, R",
            "key_skills": "Machine Learning, Statistics, Python",
            "bonus_skills": "NLP, Computer Vision, MLOps",
            "exp_years": 5
        },
        {
            "title": "Data Analyst",
            "tools": "SQL, Python, Tableau",
            "ml_type": "predictive analytics",
            "programming_languages": "SQL, Python",
            "key_skills": "SQL, Excel, Data Visualization",
            "bonus_skills": "Power BI, Python, R",
            "exp_years": 2
        },
        {
            "title": "Machine Learning Engineer",
            "tools": "Python, Scikit-learn, TensorFlow",
            "ml_type": "Machine Learning và AI",
            "programming_languages": "Python",
            "key_skills": "Python, Machine Learning, Deep Learning",
            "bonus_skills": "MLOps, Kubernetes, Spark",
            "exp_years": 4
        }
    ],
    "marketing": [
        {
            "title": "Digital Marketing Manager",
            "channels": "social media, email, SEO/SEM",
            "tools": "Google Ads, Facebook Business Manager",
            "key_skills": "SEO, SEM, Social Media Marketing",
            "bonus_skills": "Marketing Automation, CRM, Analytics",
            "exp_years": 5
        },
        {
            "title": "Content Marketing Specialist",
            "channels": "blog, social media, email",
            "tools": "WordPress, Canva, Mailchimp",
            "key_skills": "Content Writing, SEO, Social Media",
            "bonus_skills": "Video Editing, Photoshop, Google Analytics",
            "exp_years": 3
        },
        {
            "title": "Social Media Manager",
            "channels": "Facebook, Instagram, TikTok, LinkedIn",
            "tools": "Hootsuite, Buffer, Meta Business Suite",
            "key_skills": "Social Media, Content Creation, Community Management",
            "bonus_skills": "Paid Advertising, Influencer Marketing, Analytics",
            "exp_years": 3
        }
    ],
    "finance": [
        {
            "title": "Senior Financial Analyst",
            "tasks": "financial modeling, budgeting, forecasting",
            "tools": "Excel, SAP, Power BI",
            "field": "financial analysis",
            "key_skills": "Financial Modeling, Excel, Financial Reporting",
            "bonus_skills": "CFA, CPA",
            "industry": "banking, finance",
            "exp_years": 5
        },
        {
            "title": "Accountant",
            "tasks": "general ledger, reconciliation, reporting",
            "tools": "QuickBooks, Excel, ERP",
            "field": "accounting",
            "key_skills": "Accounting, Excel, Financial Reporting",
            "bonus_skills": "CPA, CIA, tax planning",
            "industry": "manufacturing, retail",
            "exp_years": 2
        },
        {
            "title": "Finance Manager",
            "tasks": "budgeting, forecasting, financial analysis, team management",
            "tools": "SAP, Oracle, Excel",
            "field": "finance management",
            "key_skills": "Financial Management, Budgeting, Team Leadership",
            "bonus_skills": "MBA, CFA, strategic planning",
            "industry": "technology, consulting",
            "exp_years": 7
        }
    ],
    "hr": [
        {
            "title": "Talent Acquisition Manager",
            "tasks": "recruitment strategy, candidate sourcing, interviewing",
            "tools": "LinkedIn Recruiter, ATS systems",
            "key_skills": "Recruitment, Talent Sourcing, Interviewing",
            "bonus_skills": "employer branding, talent pipeline development",
            "exp_years": 5
        },
        {
            "title": "HR Business Partner",
            "tasks": "employee relations, performance management, HR strategy",
            "tools": "HRIS, Workday, SAP SuccessFactors",
            "key_skills": "HR Strategy, Employee Relations, Change Management",
            "bonus_skills": "organizational development, coaching",
            "exp_years": 6
        },
        {
            "title": "Recruitment Specialist",
            "tasks": "job posting, candidate screening, interviewing, onboarding",
            "tools": "LinkedIn, job boards, ATS",
            "key_skills": "Recruitment, Candidate Assessment, Onboarding",
            "bonus_skills": "social recruiting, assessment tools",
            "exp_years": 2
        }
    ]
}

def generate_jds():
    """Generate job descriptions for all fields"""
    output_dir = Path(__file__).parent.parent / "test_data" / "jds"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_jds = []
    jd_id = 1
    
    for field, variations in JD_VARIATIONS.items():
        print(f"Generating JDs for field: {field}")
        
        # Generate Vietnamese JDs
        for variation in variations:
            template = JD_TEMPLATES[field]["vi"]
            jd_text = template.format(**variation)
            
            jd_data = {
                "id": jd_id,
                "field": field,
                "language": "vi",
                "title": variation["title"],
                "text": jd_text,
                "metadata": variation
            }
            all_jds.append(jd_data)
            
            # Save to file
            filename = f"jd_vi_{jd_id:03d}_{field}.txt"
            with open(output_dir / filename, "w", encoding="utf-8") as f:
                f.write(jd_text)
            
            jd_id += 1
        
        # Generate English JDs
        for variation in variations:
            template = JD_TEMPLATES[field]["en"]
            jd_text = template.format(**variation)
            
            jd_data = {
                "id": jd_id,
                "field": field,
                "language": "en",
                "title": variation["title"],
                "text": jd_text,
                "metadata": variation
            }
            all_jds.append(jd_data)
            
            # Save to file
            filename = f"jd_en_{jd_id:03d}_{field}.txt"
            with open(output_dir / filename, "w", encoding="utf-8") as f:
                f.write(jd_text)
            
            jd_id += 1
    
    # Save metadata
    metadata = {
        "total_jds": len(all_jds),
        "by_language": {
            "vi": sum(1 for jd in all_jds if jd["language"] == "vi"),
            "en": sum(1 for jd in all_jds if jd["language"] == "en")
        },
        "by_field": {
            field: sum(1 for jd in all_jds if jd["field"] == field)
            for field in JD_VARIATIONS.keys()
        },
        "jds": [
            {
                "id": jd["id"],
                "field": jd["field"],
                "language": jd["language"],
                "title": jd["title"],
                "filename": f"jd_{jd['language']}_{jd['id']:03d}_{jd['field']}.txt"
            }
            for jd in all_jds
        ]
    }
    
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Generated {len(all_jds)} JDs successfully!")
    print(f"   - Vietnamese JDs: {metadata['by_language']['vi']}")
    print(f"   - English JDs: {metadata['by_language']['en']}")
    print(f"   - Output directory: {output_dir}")
    print(f"   - Metadata saved to: {output_dir / 'metadata.json'}")
    
    print("\nDistribution by field:")
    for field, count in metadata['by_field'].items():
        print(f"   - {field}: {count} JDs")

if __name__ == "__main__":
    generate_jds()
