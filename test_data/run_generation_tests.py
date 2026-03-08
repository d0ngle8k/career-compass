#!/usr/bin/env python3
"""
Career Compass AI - Content Generation Test Suite
Tests generation of 100 emails and 100 cover letters (50 Vietnamese + 50 English)
Validates information extraction accuracy and checks for spelling errors.
"""

import json
import requests
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import re

# Configuration
BACKEND_URL = "http://127.0.0.1:9000"
OUTPUT_FILE = "c:\\Users\\Thanh\\Desktop\\career-compass-ai\\test_data\\generation_test_results.json"
LOGIN_EMAIL = "admin@careercompass.local"
LOGIN_PASSWORD = "admin123"

# Common Vietnamese spelling error patterns
VI_SPELLING_ERRORS = {
    "lỗi chính tả": "lỗi chính tả",
    "kiông": "không",
    "khôg": "không",
    "Kỹng": "Kỹ",
    "CẶC": "CÁ",
    "vecher": "vệ sinh",
    "Thơm": "Thơm",
}

# Test data
VI_TEST_DATA = [
    {
        "company": "Công ty Công nghệ ABC",
        "position": "Lập trình viên Backend",
        "name": "Trần Minh Đức",
        "email": "duc.tran@gmail.com",
        "phone": "0912345678",
        "recipient": "Ông Phạm Văn An",
        "skills": "Python, Django, PostgreSQL",
        "experience": 3,
    },
    {
        "company": "Tech Solutions Vietnam",
        "position": "QA Engineer",
        "name": "Lê Thị Hương",
        "email": "huong.le@gmail.com",
        "phone": "0987654321",
        "recipient": "Ms. Nguyễn Thị Mai",
        "skills": "Selenium, Java, TestNG",
        "experience": 5,
    },
    {
        "company": "NextGen Technology",
        "position": "Frontend Developer",
        "name": "Phạm Quốc Hùng",
        "email": "hung.pham@gmail.com",
        "phone": "0911111111",
        "recipient": "Ông Trần Minh Tuấn",
        "skills": "React, TypeScript, Node.js",
        "experience": 4,
    },
    {
        "company": "CloudFirst Vietnam",
        "position": "DevOps Engineer",
        "name": "Bùi Thị Lan Anh",
        "email": "lananh@gmail.com",
        "phone": "0898765432",
        "recipient": "Bà Võ Thị Hoa",
        "skills": "Kubernetes, Docker, AWS",
        "experience": 4,
    },
    {
        "company": "DataLake Corporation",
        "position": "Data Engineer",
        "name": "Ngô Văn Sơn",
        "email": "vson@gmail.com",
        "phone": "0901234567",
        "recipient": "Bà Trần Thị Liên",
        "skills": "Apache Spark, Kafka, SQL",
        "experience": 6,
    },
]

EN_TEST_DATA = [
    {
        "company": "TechCorp Inc",
        "position": "Senior Software Engineer",
        "name": "Michael Johnson",
        "email": "michael.j@gmail.com",
        "phone": "+1-555-0123",
        "recipient": "Sarah Smith",
        "skills": "Java, Spring Boot, Microservices",
        "experience": 5,
    },
    {
        "company": "StartupXYZ",
        "position": "Full Stack Developer",
        "name": "Emily Rodriguez",
        "email": "emily.r@gmail.com",
        "phone": "(555) 234-5678",
        "recipient": "David Brown",
        "skills": "React, Node.js, MongoDB",
        "experience": 4,
    },
    {
        "company": "CloudScale Solutions",
        "position": "DevOps Engineer",
        "name": "James Wilson",
        "email": "james.w@gmail.com",
        "phone": "(555) 789-0123",
        "recipient": "Lisa Anderson",
        "skills": "Kubernetes, Docker, Terraform",
        "experience": 3,
    },
    {
        "company": "SoftwarePro Inc",
        "position": "QA Automation Engineer",
        "name": "Jessica Chen",
        "email": "jessica.c@gmail.com",
        "phone": "(555) 234-5678",
        "recipient": "Robert Taylor",
        "skills": "Selenium, Python, Pytest",
        "experience": 5,
    },
    {
        "company": "AI Innovations Ltd",
        "position": "Machine Learning Engineer",
        "name": "Christopher Lee",
        "email": "chris.l@gmail.com",
        "phone": "(555) 456-7890",
        "recipient": "Amanda White",
        "skills": "TensorFlow, Python, ML",
        "experience": 4,
    },
]


def log_print(message: str, level: str = "INFO"):
    """Print log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m",
    }
    color = colors.get(level, colors["INFO"])
    reset = colors["RESET"]
    print(f"{color}[{timestamp}] {level:7s}{reset} {message}")


def get_auth_token() -> str:
    """Authenticate with backend and return access token"""
    log_print("Authenticating with backend...", "INFO")
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD},
            timeout=10,
        )
        response.raise_for_status()
        token = response.json()["data"]["access_token"]
        log_print("[OK] Authentication successful", "SUCCESS")
        return token
    except Exception as e:
        log_print(f"[FAILED] Authentication failed: {str(e)}", "ERROR")
        sys.exit(1)


def generate_test_cases() -> List[Dict]:
    """Generate 100 diverse test cases (50 VI + 50 EN)"""
    test_cases = []
    case_id = 1

    # Generate Vietnamese test cases
    for i in range(50):
        data = VI_TEST_DATA[i % len(VI_TEST_DATA)]
        
        cv_text = f"""HỒ SƠ ỨNG VIÊN

Họ và Tên: {data["name"]}
Email: {data["email"]}
Điện thoại: {data["phone"]}
Địa chỉ: Hồ Chí Minh

KINH NGHIỆM
- {data["experience"]} năm kinh nghiệm với {data["skills"]}
- Phát triển ứng dụng, tối ưu hóa hệ thống
- Làm việc với các công ty lớn

KỸ NĂNG
{data["skills"]}
Git, Linux, Agile"""

        jd_text = f"""VỊ TRÍ: {data["position"]}
CÔNG TY: {data["company"]}
Thư gửi: {data["recipient"]}

Chúng tôi tìm kiếm {data["position"]} có {data["experience"]}+ năm kinh nghiệm.
Ứng viên phải thành thạo {data["skills"]}."""

        test_cases.append(
            {
                "id": case_id,
                "language": "vi",
                "cv": cv_text,
                "jd": jd_text,
                "expected": data,
            }
        )
        case_id += 1

    # Generate English test cases
    for i in range(50):
        data = EN_TEST_DATA[i % len(EN_TEST_DATA)]
        
        cv_text = f"""PROFESSIONAL RESUME

Name: {data["name"]}
Email: {data["email"]}
Phone: {data["phone"]}
Location: United States

PROFESSIONAL EXPERIENCE
- {data["experience"]} years with {data["skills"]}
- System development and optimization
- Worked with Fortune 500 companies

TECHNICAL SKILLS
{data["skills"]}
Git, AWS, Agile Methodology"""

        jd_text = f"""Position: {data["position"]}
Company: {data["company"]}
Hiring Manager: {data["recipient"]}

We are seeking a {data["position"]} with {data["experience"]}+ years of experience.
Must have expertise in {data["skills"]}."""

        test_cases.append(
            {
                "id": case_id,
                "language": "en",
                "cv": cv_text,
                "jd": jd_text,
                "expected": data,
            }
        )
        case_id += 1

    log_print(f"Generated {len(test_cases)} test cases", "SUCCESS")
    return test_cases


def extract_extracted_metadata_accuracy(
    extracted: Dict, expected: Dict
) -> Tuple[Dict, float]:
    """Validate extracted metadata against expected values"""
    validations = {}
    
    # Check each field
    checks = {
        "name": ("candidate_name", "name"),
        "email": ("email", "email"),
        "phone": ("phone", "phone"),
        "company": ("company_name", "company"),
        "position": ("position", "position"),
        "recipient": ("recipient", "recipient"),
    }

    for check_name, (extracted_field, expected_field) in checks.items():
        extracted_value = extracted.get(extracted_field, "").strip()
        expected_value = expected.get(expected_field, "").strip()
        # Normalize for comparison
        match = extracted_value.lower() == expected_value.lower() or (
            expected_value.lower() in extracted_value.lower()
        )
        validations[check_name] = match

    accuracy = (sum(validations.values()) / len(validations)) * 100
    return validations, accuracy


def generate_emails(
    test_cases: List[Dict], token: str, headers: Dict
) -> List[Dict]:
    """Generate 100 emails and validate extraction"""
    log_print("\nGenerating 100 emails (50 Vietnamese + 50 English)...", "INFO")

    results = []
    success_count = 0
    failure_count = 0

    for i, test_case in enumerate(test_cases):
        try:
            payload = {
                "cv_text": test_case["cv"],
                "jd_text": test_case["jd"],
                "language": test_case["language"],
            }

            response = requests.post(
                f"{BACKEND_URL}/api/v1/ai/generate-email",
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()
            extracted = data["data"]["extracted_metadata"]

            validations, accuracy = extract_extracted_metadata_accuracy(
                extracted, test_case["expected"]
            )

            results.append(
                {
                    "caseId": test_case["id"],
                    "language": test_case["language"],
                    "success": True,
                    "subjectLength": len(data["data"]["email_subject"]),
                    "bodyLength": len(data["data"]["email_body"]),
                    "metadata": extracted,
                    "validations": validations,
                    "extractionAccuracy": accuracy,
                }
            )
            success_count += 1
            print(".", end="", flush=True)

        except Exception as e:
            failure_count += 1
            results.append(
                {
                    "caseId": test_case["id"],
                    "language": test_case["language"],
                    "success": False,
                    "error": str(e),
                }
            )
            print("x", end="", flush=True)

    print()
    log_print(
        f"Email generation: {success_count} successful, {failure_count} failed",
        "SUCCESS",
    )
    return results


def generate_cover_letters(
    test_cases: List[Dict], token: str, headers: Dict
) -> List[Dict]:
    """Generate 100 cover letters and validate extraction"""
    log_print(
        "Generating 100 cover letters (50 Vietnamese + 50 English)...", "INFO"
    )

    results = []
    success_count = 0
    failure_count = 0

    for i, test_case in enumerate(test_cases):
        try:
            payload = {
                "cv_text": test_case["cv"],
                "jd_text": test_case["jd"],
                "language": test_case["language"],
            }

            response = requests.post(
                f"{BACKEND_URL}/api/v1/ai/generate-cover-letter",
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()

            data = response.json()
            extracted = data["data"]["extracted_metadata"]

            validations, accuracy = extract_extracted_metadata_accuracy(
                extracted, test_case["expected"]
            )

            results.append(
                {
                    "caseId": test_case["id"],
                    "language": test_case["language"],
                    "success": True,
                    "letterLength": len(data["data"]["cover_letter"]),
                    "metadata": extracted,
                    "validations": validations,
                    "extractionAccuracy": accuracy,
                }
            )
            success_count += 1
            print(".", end="", flush=True)

        except Exception as e:
            failure_count += 1
            results.append(
                {
                    "caseId": test_case["id"],
                    "language": test_case["language"],
                    "success": False,
                    "error": str(e),
                }
            )
            print("x", end="", flush=True)

    print()
    log_print(
        f"Cover letter generation: {success_count} successful, {failure_count} failed",
        "SUCCESS",
    )
    return results


def calculate_statistics(results: List[Dict]) -> Dict:
    """Calculate statistics from results"""
    successful = [r for r in results if r.get("success", False)]
    
    if not successful:
        return {
            "totalGenerated": 0,
            "successRate": 0,
            "vietnameseSuccess": 0,
            "englishSuccess": 0,
            "avgExtractionAccuracy": 0,
            "extractionBreakdown": {},
        }

    vi_success = len([r for r in successful if r["language"] == "vi"])
    en_success = len([r for r in successful if r["language"] == "en"])

    # Calculate field-wise accuracy
    field_stats = {
        "name": 0,
        "email": 0,
        "phone": 0,
        "company": 0,
        "position": 0,
        "recipient": 0,
    }

    for result in successful:
        if "validations" in result:
            for field, is_valid in result["validations"].items():
                if is_valid:
                    field_stats[field] += 1

    breakdown = {
        field: (count / len(successful)) * 100
        for field, count in field_stats.items()
    }

    avg_accuracy = (
        sum(r.get("extractionAccuracy", 0) for r in successful)
        / len(successful)
    )

    return {
        "totalGenerated": len(successful),
        "successRate": (len(successful) / len(results)) * 100,
        "vietnameseSuccess": vi_success,
        "englishSuccess": en_success,
        "avgExtractionAccuracy": avg_accuracy,
        "extractionBreakdown": breakdown,
    }


def main():
    """Main test execution"""
    print(
        "\n" + "=" * 70
        + "\nCareer Compass AI - Content Generation Test Suite"
        + "\nBackend: " + BACKEND_URL + "\n" + "=" * 70 + "\n"
    )

    # Step 1: Authenticate
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Step 2: Generate test cases
    log_print("Generating test data...", "INFO")
    test_cases = generate_test_cases()

    # Step 3: Generate emails
    print()
    email_results = generate_emails(test_cases, token, headers)

    # Step 4: Generate cover letters
    print()
    cover_results = generate_cover_letters(test_cases, token, headers)

    # Step 5: Calculate statistics
    log_print("Analyzing results...", "INFO")
    email_stats = calculate_statistics(email_results)
    cover_stats = calculate_statistics(cover_results)

    # Step 6: Create report
    report = {
        "testSummary": {
            "timestamp": datetime.now().isoformat(),
            "totalTestCases": len(test_cases),
            "emailTests": {
                "total": len(email_results),
                "successful": len([r for r in email_results if r.get("success")]),
                "failed": len([r for r in email_results if not r.get("success")]),
            },
            "coverLetterTests": {
                "total": len(cover_results),
                "successful": len([r for r in cover_results if r.get("success")]),
                "failed": len([r for r in cover_results if not r.get("success")]),
            },
        },
        "emailStats": email_stats,
        "coverLetterStats": cover_stats,
        "emailResults": email_results,
        "coverLetterResults": cover_results,
    }

    # Save report
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log_print(f"Report saved to: {OUTPUT_FILE}", "SUCCESS")

    # Display summary
    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)

    print("\n=== EMAIL GENERATION ===")
    print(f"  Success Rate: {email_stats['successRate']:.2f}% ({email_stats['totalGenerated']}/100)")
    print(f"  Vietnamese: {email_stats['vietnameseSuccess']}/50, English: {email_stats['englishSuccess']}/50")
    print(f"  Avg Extraction Accuracy: {email_stats['avgExtractionAccuracy']:.2f}%")
    print("  Field Accuracy:")
    for field, acc in email_stats["extractionBreakdown"].items():
        print(f"    - {field.capitalize()}: {acc:.2f}%")

    print("\n=== COVER LETTER GENERATION ===")
    print(f"  Success Rate: {cover_stats['successRate']:.2f}% ({cover_stats['totalGenerated']}/100)")
    print(f"  Vietnamese: {cover_stats['vietnameseSuccess']}/50, English: {cover_stats['englishSuccess']}/50")
    print(f"  Avg Extraction Accuracy: {cover_stats['avgExtractionAccuracy']:.2f}%")
    print("  Field Accuracy:")
    for field, acc in cover_stats["extractionBreakdown"].items():
        print(f"    - {field.capitalize()}: {acc:.2f}%")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
