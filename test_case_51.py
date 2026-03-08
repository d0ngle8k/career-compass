#!/usr/bin/env python3
import json
import requests

# Get auth token first
print("Getting auth token...")
try:
    auth_response = requests.post(
        'http://localhost:9000/api/v1/auth/login',
        json={
            'email': 'admin@careercompass.local',
            'password': 'admin123'
        },
        timeout=5
    )
    auth_response.raise_for_status()
    token = auth_response.json()['data']['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print("Auth successful")
except Exception as e:
    print(f"Auth failed: {e}")
    exit(1)

# Case 51 uses EN_TEST_DATA[0 % len(EN_TEST_DATA)]
# which is TechCorp Inc / Senior Software Engineer

data = {
    "company": "TechCorp Inc",
    "position": "Senior Software Engineer",
    "name": "Michael Johnson",
    "email": "michael.j@gmail.com",
    "phone": "+1-555-0123",
    "recipient": "Sarah Smith",
    "skills": "Java, Spring Boot, Microservices",
    "experience": 5,
}

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

print("=== TEST CASE 51 ===")
print(f"CV Length: {len(cv_text)}")
print(f"JD Length: {len(jd_text)}\n")

# Send request to backend
try:
    response = requests.post('http://localhost:9000/api/v1/content/generate-email', json={
        'cv_text': cv_text,
        'jd_text': jd_text,
        'language': 'en',
        'style': 'casual'
    }, headers=headers, timeout=5)
    
    print('Status:', response.status_code)
    if response.status_code == 200:
        result = response.json()
        print('Full Response:', json.dumps(result, indent=2))
    else:
        print('Error Response:')
        print(response.text[:500])
except Exception as e:
    print('Request Error:', str(e))
    import traceback
    traceback.print_exc()
