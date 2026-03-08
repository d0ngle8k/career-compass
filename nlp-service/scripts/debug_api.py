import requests
import json
from pathlib import Path

# Load test CV and JD
cv_path = Path("test_data/cvs/cv_vi_001_software.txt")
jd_path = Path("test_data/jds/jd_vi_001_software.txt")

cv_text = cv_path.read_text(encoding="utf-8")
jd_text = jd_path.read_text(encoding="utf-8")

print(f"CV length: {len(cv_text)}")
print(f"JD length: {len(jd_text)}")
print("\n" + "="*80)

# Test scoring
url = "http://127.0.0.1:8001/score-cv"
payload = {
    "cv_text": cv_text,
    "jd_text": jd_text
}

print(f"\nCalling {url}")
response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

# Test NER
print("\n" + "="*80)
url_ner = "http://127.0.0.1:8001/ner/vi"
payload_ner = {"text": cv_text}

print(f"\nCalling {url_ner}")
response_ner = requests.post(url_ner, json=payload_ner)
print(f"Status: {response_ner.status_code}")
result = response_ner.json()
print(f"Entities found: {len(result.get('entities', []))}")
if result.get('entities'):
    print("First 5 entities:")
    for ent in result['entities'][:5]:
        print(f"  - {ent}")
