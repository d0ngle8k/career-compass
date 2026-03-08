"""
Generate 100 test CVs (50 Vietnamese, 50 English) for CV scoring evaluation
"""
import json
import random
from pathlib import Path
from typing import List, Dict

# Vietnamese CV data
VI_NAMES = [
    "Nguyễn Văn An", "Trần Thị Bình", "Lê Hoàng Châu", "Phạm Minh Đức", 
    "Hoàng Thị Em", "Vũ Văn Phong", "Đặng Thị Giang", "Bùi Minh Hải",
    "Đinh Thị Lan", "Đỗ Văn Khoa", "Ngô Thị Linh", "Dương Văn Minh",
    "Phan Thị Nga", "Tô Văn Nam", "Lý Thị Oanh", "Mai Văn Phúc",
    "Hồ Thị Quỳnh", "Võ Văn Sơn", "Cao Thị Trang", "Trương Văn Tùng",
    "Lâm Thị Uyên", "Huỳnh Văn Vinh", "Chu Thị Xuân", "Hà Văn Yên",
    "La Thị Hoa", "Tạ Văn Hùng", "Lương Thị Hạnh", "Phạm Văn Kiên",
    "Trịnh Thị Liên", "Doãn Văn Long", "Nông Thị Mai", "Quách Văn Nam",
    "Văn Thị Nhung", "Sa Văn Phong", "Tào Thị Quyên", "Âu Văn Rạng",
    "Ông Thị Sáng", "Ứng Văn Tâm", "Thái Thị Thảo", "Bạch Văn Thanh",
    "Đoàn Thị Thủy", "Hứa Văn Tiến", "Nghiêm Thị Tú", "Nhan Văn Tùng",
    "Ưng Thị Uyên", "Từ Văn Vân", "Gia Thị Vân", "Kiều Văn Việt",
    "La Thị Xuyến", "Tống Văn Yên"
]

EN_NAMES = [
    "John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis",
    "David Wilson", "Jessica Miller", "James Anderson", "Jennifer Taylor",
    "Robert Thomas", "Linda Jackson", "William White", "Patricia Harris",
    "Richard Martin", "Barbara Thompson", "Joseph Garcia", "Susan Martinez",
    "Thomas Robinson", "Nancy Clark", "Charles Rodriguez", "Karen Lewis",
    "Christopher Lee", "Betty Walker", "Daniel Hall", "Lisa Allen",
    "Matthew Young", "Helen King", "Mark Wright", "Sandra Lopez",
    "Donald Scott", "Ashley Green", "Paul Adams", "Donna Baker",
    "Steven Nelson", "Carol Carter", "Andrew Mitchell", "Michelle Roberts",
    "Kenneth Turner", "Emily Phillips", "Joshua Campbell", "Amanda Parker",
    "Kevin Evans", "Melissa Edwards", "Brian Collins", "Deborah Stewart",
    "George Morris", "Stephanie Rogers", "Edward Reed", "Rebecca Cook",
    "Ronald Morgan", "Laura Bailey"
]

VI_SKILLS_BY_FIELD = {
    "software": ["Python", "Java", "JavaScript", "React", "Node.js", "SQL", "MongoDB", "Docker", "Kubernetes", "AWS", "Git", "Agile", "Scrum", "REST API", "GraphQL", "TypeScript", "Vue.js", "Angular", "Spring Boot", "Django"],
    "data": ["Python", "R", "SQL", "Tableau", "Power BI", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Spark", "Hadoop", "Data Visualization", "Statistics", "Excel", "ETL", "Big Data", "AI"],
    "marketing": ["SEO", "SEM", "Google Analytics", "Facebook Ads", "Content Marketing", "Social Media", "Email Marketing", "Photoshop", "Canva", "Video Editing", "Brand Management", "Market Research", "Public Relations", "Copywriting", "Google Ads", "Customer Insights", "CRM", "Adobe Suite", "WordPress", "HTML/CSS"],
    "finance": ["Excel", "Financial Analysis", "Accounting", "SAP", "QuickBooks", "Financial Modeling", "Budgeting", "Forecasting", "Tax Planning", "Risk Management", "Investment Analysis", "IFRS", "VAS", "Audit", "Cost Analysis", "Bloomberg Terminal", "SQL", "Power BI", "Treasury Management", "Corporate Finance"],
    "hr": ["Recruitment", "Employee Relations", "Training & Development", "Performance Management", "Labor Law", "HRIS", "Talent Acquisition", "Compensation & Benefits", "Organizational Development", "HR Analytics", "Payroll", "Conflict Resolution", "Interviewing", "Onboarding", "Excel", "Employee Engagement", "Workforce Planning", "Change Management", "HR Policies", "Culture Building"]
}

EN_SKILLS_BY_FIELD = VI_SKILLS_BY_FIELD.copy()

VI_JOB_TITLES = {
    "software": ["Lập trình viên Python", "Lập trình viên Java", "Full-stack Developer", "Backend Developer", "Frontend Developer", "Mobile Developer", "DevOps Engineer", "Software Engineer", "Web Developer", "Software Architect"],
    "data": ["Data Analyst", "Data Scientist", "Machine Learning Engineer", "Data Engineer", "Business Intelligence Analyst", "AI Engineer", "Big Data Engineer", "Research Scientist", "Analytics Manager", "Data Consultant"],
    "marketing": ["Marketing Manager", "Digital Marketing Specialist", "Social Media Manager", "Content Creator", "SEO Specialist", "Brand Manager", "Marketing Analyst", "Growth Hacker", "PR Manager", "Product Marketing Manager"],
    "finance": ["Kế toán viên", "Phân tích tài chính", "Kiểm toán viên", "Quản lý tài chính", "Chuyên viên thuế", "Chuyên viên ngân hàng", "Phân tích đầu tư", "Controller", "CFO", "Treasury Analyst"],
    "hr": ["HR Manager", "Recruitment Specialist", "HR Business Partner", "Training Manager", "Compensation & Benefits Specialist", "Talent Acquisition Manager", "HR Analyst", "Employee Relations Manager", "HRBP", "Chief People Officer"]
}

EN_JOB_TITLES = {
    "software": ["Python Developer", "Java Developer", "Full-stack Developer", "Backend Developer", "Frontend Developer", "Mobile Developer", "DevOps Engineer", "Software Engineer", "Web Developer", "Software Architect"],
    "data": ["Data Analyst", "Data Scientist", "Machine Learning Engineer", "Data Engineer", "Business Intelligence Analyst", "AI Engineer", "Big Data Engineer", "Research Scientist", "Analytics Manager", "Data Consultant"],
    "marketing": ["Marketing Manager", "Digital Marketing Specialist", "Social Media Manager", "Content Creator", "SEO Specialist", "Brand Manager", "Marketing Analyst", "Growth Hacker", "PR Manager", "Product Marketing Manager"],
    "finance": ["Accountant", "Financial Analyst", "Auditor", "Finance Manager", "Tax Specialist", "Banking Specialist", "Investment Analyst", "Controller", "CFO", "Treasury Analyst"],
    "hr": ["HR Manager", "Recruitment Specialist", "HR Business Partner", "Training Manager", "Compensation & Benefits Specialist", "Talent Acquisition Manager", "HR Analyst", "Employee Relations Manager", "HRBP", "Chief People Officer"]
}

VI_COMPANIES = [
    "FPT Software", "Viettel", "VNPT", "VNG Corporation", "Tiki", "Lazada Vietnam",
    "Shopee Vietnam", "Grab Vietnam", "Momo", "VPBank", "Vietcombank", "BIDV",
    "Vingroup", "Masan Group", "PNJ", "The Gioi Di Dong", "Dien Quan", "Saigon Co.op",
    "VinFast", "Techcombank", "MB Bank", "ACB", "Sendo", "Got It", "Zalo", "Base.vn"
]

EN_COMPANIES = [
    "Google", "Apple", "Microsoft", "Amazon", "Meta", "Netflix", "Tesla", "IBM",
    "Oracle", "SAP", "Adobe", "Salesforce", "Intel", "Cisco", "HP", "Dell",
    "Deloitte", "PwC", "EY", "KPMG", "McKinsey", "BCG", "Accenture", "Capgemini",
    "Goldman Sachs", "JP Morgan", "Morgan Stanley", "Citibank"
]

VI_UNIVERSITIES = [
    "Đại học Bách Khoa Hà Nội", "Đại học Quốc Gia Hà Nội", "Đại học Bách Khoa TP.HCM",
    "Đại học Quốc Gia TP.HCM", "Đại học Kinh tế Quốc dân", "Đại học Ngoại Thương",
    "Đại học Công nghệ - ĐHQGHN", "Đại học Khoa học Tự nhiên", "Đại học FPT",
    "Đại học RMIT", "Đại học Tôn Đức Thắng", "Đại học Hutech", "Đại học Văn Lang",
    "Đại học Ngân hàng TP.HCM", "Đại học Kinh tế TP.HCM"
]

EN_UNIVERSITIES = [
    "Massachusetts Institute of Technology", "Stanford University", "Harvard University",
    "University of California, Berkeley", "Carnegie Mellon University", "University of Oxford",
    "University of Cambridge", "ETH Zurich", "National University of Singapore",
    "Tsinghua University", "University of Toronto", "Imperial College London",
    "University of Michigan", "Cornell University", "Yale University"
]

DEGREES = {
    "vi": ["Cử nhân", "Thạc sĩ", "Tiến sĩ", "Kỹ sư"],
    "en": ["Bachelor", "Master", "PhD", "Engineer"]
}

MAJORS = {
    "software": {
        "vi": ["Công nghệ Thông tin", "Khoa học Máy tính", "Kỹ thuật Phần mềm", "Hệ thống Thông tin"],
        "en": ["Computer Science", "Software Engineering", "Information Technology", "Information Systems"]
    },
    "data": {
        "vi": ["Khoa học Dữ liệu", "Toán - Tin ứng dụng", "Thống kê", "Trí tuệ Nhân tạo"],
        "en": ["Data Science", "Applied Mathematics", "Statistics", "Artificial Intelligence"]
    },
    "marketing": {
        "vi": ["Marketing", "Quản trị Kinh doanh", "Truyền thông", "Quan hệ Công chúng"],
        "en": ["Marketing", "Business Administration", "Communications", "Public Relations"]
    },
    "finance": {
        "vi": ["Tài chính - Ngân hàng", "Kế toán", "Kinh tế", "Quản trị Kinh doanh"],
        "en": ["Finance", "Accounting", "Economics", "Business Administration"]
    },
    "hr": {
        "vi": ["Quản trị Nhân sự", "Tâm lý học", "Quản trị Kinh doanh", "Xã hội học"],
        "en": ["Human Resource Management", "Psychology", "Business Administration", "Sociology"]
    }
}

def generate_vi_cv(name: str, field: str, experience_years: int) -> Dict:
    """Generate a Vietnamese CV"""
    skills = random.sample(VI_SKILLS_BY_FIELD[field], k=random.randint(8, 15))
    job_title = random.choice(VI_JOB_TITLES[field])
    company = random.choice(VI_COMPANIES)
    university = random.choice(VI_UNIVERSITIES)
    degree = random.choice(DEGREES["vi"])
    major = random.choice(MAJORS[field]["vi"])
    
    # Generate experience descriptions
    experiences = []
    years_left = experience_years
    while years_left > 0:
        exp_years = min(random.randint(1, 4), years_left)
        exp_company = random.choice(VI_COMPANIES)
        exp_title = random.choice(VI_JOB_TITLES[field])
        experiences.append({
            "title": exp_title,
            "company": exp_company,
            "duration": f"{exp_years} năm",
            "description": f"Làm việc tại {exp_company} với vai trò {exp_title}"
        })
        years_left -= exp_years
    
    cv_text = f"""HỌ VÀ TÊN: {name}

VỊ TRÍ ỨNG TUYỂN: {job_title}

THÔNG TIN LIÊN HỆ:
Email: {name.lower().replace(' ', '.')}@email.com
Điện thoại: {random.randint(90000000, 999999999):010d}
Địa chỉ: {random.choice(['Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ'])}

HỌC VẤN:
{degree} {major}
{university}
Tốt nghiệp năm {2024 - experience_years - random.randint(0, 2)}
GPA: {random.uniform(3.0, 4.0):.2f}/4.0

KINH NGHIỆM LÀM VIỆC: {experience_years} năm
"""
    
    for exp in experiences:
        cv_text += f"\n{exp['title']} - {exp['company']}\n{exp['duration']}\n{exp['description']}\n"
    
    cv_text += f"\nKỸ NĂNG:\n{', '.join(skills)}\n"
    
    # Add some achievements
    achievements = [
        "Hoàn thành dự án đúng tiến độ và ngân sách",
        "Cải thiện hiệu suất hệ thống 30%",
        "Đào tạo và hướng dẫn 5+ nhân viên mới",
        "Nhận giải thưởng nhân viên xuất sắc",
        "Tối ưu hóa quy trình làm việc nhóm"
    ]
    cv_text += f"\nTHÀNH TỰU:\n- " + "\n- ".join(random.sample(achievements, k=random.randint(2, 4)))
    
    cv_text += f"\n\nNGÔN NGỮ:\nTiếng Việt: Bản ngữ\nTiếng Anh: {random.choice(['Giao tiếp', 'Trung cấp', 'Khá', 'Tốt', 'Thành thạo'])}\n"
    
    return {
        "name": name,
        "language": "vi",
        "field": field,
        "experience_years": experience_years,
        "text": cv_text
    }

def generate_en_cv(name: str, field: str, experience_years: int) -> Dict:
    """Generate an English CV"""
    skills = random.sample(EN_SKILLS_BY_FIELD[field], k=random.randint(8, 15))
    job_title = random.choice(EN_JOB_TITLES[field])
    company = random.choice(EN_COMPANIES)
    university = random.choice(EN_UNIVERSITIES)
    degree = random.choice(DEGREES["en"])
    major = random.choice(MAJORS[field]["en"])
    
    # Generate experience descriptions
    experiences = []
    years_left = experience_years
    while years_left > 0:
        exp_years = min(random.randint(1, 4), years_left)
        exp_company = random.choice(EN_COMPANIES)
        exp_title = random.choice(EN_JOB_TITLES[field])
        experiences.append({
            "title": exp_title,
            "company": exp_company,
            "duration": f"{exp_years} year{'s' if exp_years > 1 else ''}",
            "description": f"Worked at {exp_company} as {exp_title}"
        })
        years_left -= exp_years
    
    cv_text = f"""NAME: {name}

POSITION: {job_title}

CONTACT INFORMATION:
Email: {name.lower().replace(' ', '.')}@email.com
Phone: +1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}
Location: {random.choice(['New York, NY', 'San Francisco, CA', 'Seattle, WA', 'Boston, MA', 'Austin, TX', 'Chicago, IL'])}

EDUCATION:
{degree} of {major}
{university}
Graduated: {2024 - experience_years - random.randint(0, 2)}
GPA: {random.uniform(3.0, 4.0):.2f}/4.0

WORK EXPERIENCE: {experience_years} years
"""
    
    for exp in experiences:
        cv_text += f"\n{exp['title']} - {exp['company']}\n{exp['duration']}\n{exp['description']}\n"
    
    cv_text += f"\nSKILLS:\n{', '.join(skills)}\n"
    
    # Add some achievements
    achievements = [
        "Delivered projects on time and within budget",
        "Improved system performance by 30%",
        "Trained and mentored 5+ junior developers",
        "Received Employee of the Year award",
        "Optimized team workflow processes",
        "Led cross-functional team of 10+ members"
    ]
    cv_text += f"\nACHIEVEMENTS:\n- " + "\n- ".join(random.sample(achievements, k=random.randint(2, 4)))
    
    cv_text += f"\n\nLANGUAGES:\nEnglish: Native\n{random.choice(['Spanish', 'French', 'German', 'Chinese', 'Japanese'])}: {random.choice(['Basic', 'Intermediate', 'Advanced', 'Fluent'])}\n"
    
    return {
        "name": name,
        "language": "en",
        "field": field,
        "experience_years": experience_years,
        "text": cv_text
    }

def main():
    """Generate 100 CVs (50 Vietnamese, 50 English)"""
    output_dir = Path(__file__).parent.parent / "test_data" / "cvs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_cvs = []
    fields = list(VI_SKILLS_BY_FIELD.keys())
    
    # Generate 50 Vietnamese CVs
    print("Generating 50 Vietnamese CVs...")
    for i in range(50):
        name = VI_NAMES[i]
        field = fields[i % len(fields)]
        experience_years = random.randint(1, 15)
        cv = generate_vi_cv(name, field, experience_years)
        all_cvs.append(cv)
        
        # Save individual CV
        filename = f"cv_vi_{i+1:03d}_{field}.txt"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(cv["text"])
    
    # Generate 50 English CVs
    print("Generating 50 English CVs...")
    for i in range(50):
        name = EN_NAMES[i]
        field = fields[i % len(fields)]
        experience_years = random.randint(1, 15)
        cv = generate_en_cv(name, field, experience_years)
        all_cvs.append(cv)
        
        # Save individual CV
        filename = f"cv_en_{i+1:03d}_{field}.txt"
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(cv["text"])
    
    # Save metadata
    metadata = {
        "total_cvs": len(all_cvs),
        "vietnamese_cvs": 50,
        "english_cvs": 50,
        "fields": fields,
        "cvs": [
            {
                "id": idx + 1,
                "name": cv["name"],
                "language": cv["language"],
                "field": cv["field"],
                "experience_years": cv["experience_years"],
                "filename": f"cv_{cv['language']}_{(idx % 50) + 1:03d}_{cv['field']}.txt"
            }
            for idx, cv in enumerate(all_cvs)
        ]
    }
    
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Generated 100 CVs successfully!")
    print(f"   - Vietnamese CVs: 50")
    print(f"   - English CVs: 50")
    print(f"   - Output directory: {output_dir}")
    print(f"   - Metadata saved to: {output_dir / 'metadata.json'}")
    
    # Print distribution by field
    print("\nDistribution by field:")
    for field in fields:
        count = sum(1 for cv in all_cvs if cv["field"] == field)
        print(f"   - {field}: {count} CVs")

if __name__ == "__main__":
    main()
