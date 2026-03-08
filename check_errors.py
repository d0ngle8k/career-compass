import json

with open('test_data/generation_test_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== FAILED EMAIL CASES ===")
for result in data['emailResults']:
    if not result.get('success'):
        print(f"Case #{result['caseId']} ({result['language'].upper()}): {result.get('error', 'Unknown')}")

print("\n=== FAILED COVER LETTER CASES ===")
for result in data['coverLetterResults']:
    if not result.get('success'):
        print(f"Case #{result['caseId']} ({result['language'].upper()}): {result.get('error', 'Unknown')}")
