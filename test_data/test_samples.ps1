# Test Data Generator - Creates diverse CV and JD samples for testing
# This generates realistic CV and JD text with varied formats

$Vietnamese_CVs = @(
    @{
        cv = @"
HỒ SƠ ỨNG VIÊN

Họ và Tên: Trần Minh Đức
Email: minh.duc@gmail.com
Điện thoại: 0912345678
Địa chỉ: 123 Đường Nguyễn Huệ, Quận 1, TP.HCM

KINH NGHIỆM LÀM VIỆC
- 3 năm kinh nghiệm với Python, Django, PostgreSQL
- Phát triển API RESTful, tối ưu hóa cơ sở dữ liệu
- Làm việc với Docker, Linux, Git

KỸ NĂNG
Ngôn ngữ: Python, JavaScript, SQL
Framework: Django, FastAPI, React
Database: PostgreSQL, MongoDB
Tools: Docker, Git, AWS
"@
        jd = @"
VỊ TRÍ: Lập trình viên Backend (Python)
CÔNG TY: Công ty Công nghệ ABC
Thư gửi: Ông Phạm Văn An

Chúng tôi tìm kiếm một lập trình viên backend giàu kinh nghiệm với 3-5 năm làm việc. Ứng viên phải thành thạo Python, Django, PostgreSQL.
"@
    },
    @{
        cv = @"
CV - NGHiỀP VỤ CHUYÊN MÔN

Tên: Lê Thị Hương
Liên hệ: huana@email.com
SĐT: 0987654321
Nơi ở: 456 Lê Lợi, Hà Nội

QUÃNG THỜI GIAN CÔNG VIỆC
5 năm làm QA Engineer tại các công ty lớn
Kiông nghiệm với Selenium, Java, TestNG
Quản lý test cases, tự động hóa testing

CHUYÊN MÔN KỸ NĂNG
QA Automation, Manual Testing, Selenium (typo: Selennium)
JavaScript, Java, Python
Jira, GitHub, Linux
"@
        jd = @"
Tuyển dụng: QA Engineer (Automation)
Công ty: Tech Solutions Vietnam
Gửi đến: Ms. Nguyễn Thị Mai

Cần một QA Engineer có kinh nghiệm 5+ năm với Selenium và Java. Ứng viên sẽ làm việc với team development để đảm bảo chất lượng sản phẩm.
"@
    },
    @{
        cv = @"
PROFILE NHÂN VIÊN

Name in Vietnamese: Phạm Quốc Hùng
Email Contact: hung.pham@company.com
Phone Number: 0911111111
Location: 789 Đường Pasteur, Q3, TPHCM

WORK EXPERIENCE
2 năm làm Frontend Developer tại NextGen Technology
Phát triển ứng dụng React, Vue.js
Làm việc với Tailwind CSS, Bootstrap

SKILLS & EXPERTISE
React, Vue.js, TypeScript, HTML/CSS
Node.js, REST APIs
Git, Docker, Webpack
"@
        jd = @"
Position: Senior Frontend Developer
Company: Global Tech Corp Vietnam
Hiring Manager: John Smith

We are seeking a Senior Frontend Developer with 5+ years of experience in React or Vue.js. Must have strong understanding of TypeScript and modern web development practices. Knowledge of containerization with Docker is a plus.
"@
    },
    @{
        cv = @"
HỒSƠ CHUYÊN VIÊN

Họ tên: Bùi Thị Lan Anh
Email: lananh@gmail.com  
Điện thoại: 0898765432
Địa chỉ: 321 Nguyễn Chí Thanh, Hà Nội

KINH NGHIỆM
4 năm làm DevOps Engineer
Quản lý hạ tầng Cloud: AWS, Azure, GCP
Triển khai CI/CD pipelines với Jenkins, GitLab
Containerization: Docker, Kubernetes

KỸNG NĂNG (Error: Kỹng -> Kỹ)
Linux Administration, Docker, Kubernetes
AWS: EC2, RDS, S3, Lambda
Terraform, Ansible
Python scripting
"@
        jd = @"
Vị trí: Chuyên viên DevOps
Công ty: CloudFirst Vietnam
Liên hệ: Ông Trần Minh Tuấn

Tuyển dụng DevOps Engineer có 4-6 năm kinh nghiệm. Ứng viên phải thành thạo Kubernetes, Docker, AWS và Infrastructure as Code.
"@
    },
    @{
        cv = @"
THÔNG TIN CẶC NHÂN (Typo: CẶC -> CÁ)

Họ và tên: Ngô Văn Sơn
Email: vson@email.com
Phone: 0901234567
Nơi cư trú: 654 Bà Triệu, Hà Nội

KINH NGHIỆM LÀM VIỆC
6 năm Data Engineer tại công ty công nghệ
Xây dựng data pipelines với Apache Spark, Hadoop
SQL optimization, data warehouse (Snowflake, BigQuery)
Python, Scala programming

KỸ NĂNG
Big Data: Spark, Hadoop, Kafka
Cloud: AWS, Google Cloud
Languages: Python, Scala, SQL
Tools: Airflow, Tableau, Git
"@
        jd = @"
Chơi vị: Data Engineer (Typo: Chơi -> Chức)
Công ty tuyển: DataLake Corporation
Người liên lạ: Bà Võ Thị Hoa

Tìm Data Engineer có 5+ năm với Apache Spark, Hadoop, Kafka. Kỹ năng SQL và Python bắt buộc. Kiến thức về cloud platforms (AWS, GCP) là lợi thế.
"@
    }
)

$English_CVs = @(
    @{
        cv = @"
PROFESSIONAL RESUME

Name: Michael Johnson
Email: michael.j@gmail.com
Phone: +1-555-0123
Location: San Francisco, CA

PROFESSIONAL EXPERIENCE
Senior Software Engineer - 5+ years
- Specialized in Java, Spring Boot, Microservices
- Architected scalable backend systems
- Led team of 4 engineers

TECHNICAL SKILLS
Languages: Java, Python, JavaScript
Frameworks: Spring Boot, Spring Cloud
Databases: PostgreSQL, MongoDB, Redis
Cloud: AWS, Docker, Kubernetes
"@
        jd = @"
Position: Senior Software Engineer
Company: TechCorp Inc
Hiring Manager: Sarah Smith

Hiring for a Senior Software Engineer with 5+ years of experience in Java and microservices architecture. Must have experience with Spring Boot, Docker, and AWS. Lead technical discussions and mentor junior developers.
"@
    },
    @{
        cv = @"
CV - SOFTWARE DEVELOPMENT

Name: Emily Rodriguez
Contact: emily.r@company.com
Phone: 0912-555-0456
Address: New York, NY

CAREER HISTORY
4 years as Full Stack Developer
- React, Node.js, MongoDB development
- RESTful API design and implementation
- PostgreSQL optimization

COMPETENCIES & SKILLS
Frontend: React, Vue.js, TypeScript, HTML5, CSS3
Backend: Node.js, Express, Python
Databases: PostgreSQL, MongoDB
DevOps: Docker, GitHub Actions, Heroku
"@
        jd = @"
Role: Full Stack Developer
Organization: StartupXYZ
Contact person: David Brown

Seeking a Full Stack Developer with 3+ years experience. Must be proficient in React, Node.js, and have database knowledge. Excellent problem-solving skills required. Work with agile teams.
"@
    },
    @{
        cv = @"
CURRICULUM VITAE

Full Name: James Wilson
Email: james.wilson@gmail.com
Mobile: (555) 789-0123
Location: Seattle, Washington

WORK EXPERIENCE
DevOps Engineer - 3 years
- Infrastructure as Code with Terraform
- CI/CD pipeline implementation using Jenkins
- Kubernetes orchastration (misspelled: orchastration)
- Linux and Cloud administration

CORE COMPETENCIES
Cloud Platforms: AWS, GCP, Azure
Containerization: Docker, Kubernetes, Helm
Languages: Python, Bash, Go
Tools: Terraform, Ansible, Jenkins, GitLab CI
"@
        jd = @"
Job Title: DevOps Engineer
Company: CloudScale Solutions
Manager: Lisa Anderson

Looking for DevOps Engineer with 3-5 years experience in Kubernetes, Docker, and infrastructure automation. Strong understanding of CI/CD principles. AWS or GCP experience preferred.
"@
    },
    @{
        cv = @"
PROFESSIONAL PROFILE

Name: Jessica Chen
Email: jessica.c@email.com
Contact Number: (555) 234-5678
Location: Boston, Massachusetts

CAREER BACKGROUND
5 years in Quality Assurance
- Automated testing with Selenium and Python
- Test framework development
- Agile/Scrum methodolgy experience (typo: methodolgy -> methodology)

TECHNICAL EXPERTISE
Test Automation: Selenium, TestNG, Pytest
Languages: Python, Java, JavaScript
Frameworks: Cucumber, Robot Framework
Tools: Jira, Git, Jenkins
Databases: MySQL, PostgreSQL
"@
        jd = @"
Position: QA Automation Engineer
Company: SoftwarePro Inc
Hiring Lead: Robert Taylor

Hiring QA Automation Engineer with 5+ years experience. Must have strong Selenium and Python skills. Experience with CI/CD pipelines and Agile methodologies is essential.
"@
    },
    @{
        cv = @"
CURRICULUM VITAE

Full Name: Christopher Lee
Email: chris.lee@gmail.com
Phone: (555) 456-7890
Address: Los Angeles, California

PROFESSIONAL EXPERIENCE
Data Scientist - 4 years
- Machine Learning model development with TensorFlow
- Data analysis using Pandas and NumPy
- SQL query optimization

SKILLS AND EXPERTISE
Programming: Python, R, SQL
ML Libraries: TensorFlow, Scikit-learn, XGBoost
Data Visualization: Matplotlib, Seaborn, Tableau
Cloud: AWS SageMaker, Google Cloud ML
Databases: PostgreSQL, MongoDB, Redshift
"@
        jd = @"
Role: Machine Learning Engineer
Company: AI Innovations Ltd
Hiring Manager: Amanda White

We need a Machine Learning Engineer with 4+ years experience in Python and deep learning frameworks (TensorFlow or PyTorch). Experience with data pipelines and cloud ML platforms required.
"@
    }
)

# Export for use in main test script
Export-ModuleMember -Variable @("Vietnamese_CVs", "English_CVs")
