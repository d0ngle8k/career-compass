"""
Detailed analysis of scoring results to identify improvement opportunities
"""
import json
import sys
import os
from collections import defaultdict

# Load test results
results_path = "C:/Users/Thanh/Desktop/career-compass-ai/nlp-service/test_data/scoring_test_results.json"
with open(results_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    results = data.get('results', data)  # Handle both formats

print("=" * 80)
print("DETAILED SCORING ANALYSIS")
print("=" * 80)

# Analyze score distribution
scores = [r['score'] for r in results]
print(f"\nScore Distribution:")
print(f"  < 40: {sum(1 for s in scores if s < 40)} CVs")
print(f"  40-50: {sum(1 for s in scores if 40 <= s < 50)} CVs")
print(f"  50-60: {sum(1 for s in scores if 50 <= s < 60)} CVs")
print(f"  60-70: {sum(1 for s in scores if 60 <= s < 70)} CVs")
print(f"  70-80: {sum(1 for s in scores if 70 <= s < 80)} CVs")
print(f"  80-90: {sum(1 for s in scores if 80 <= s < 90)} CVs")
print(f"  >= 90: {sum(1 for s in scores if s >= 90)} CVs")

# Find top performers
top_10 = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
print(f"\n" + "=" * 80)
print("TOP 10 SCORING CVs:")
print("=" * 80)
for i, r in enumerate(top_10, 1):
    print(f"\n{i}. CV#{r['cv_id']} {r['cv_name']} vs {r['jd_title']}")
    print(f"   Score: {r['score']}/100")
    print(f"   Language: {r['cv_language']}")
    print(f"   Field: {r['cv_field']}")
    print(f"   Experience: {r['cv_experience_years']} years")

# Find bottom performers
bottom_10 = sorted(results, key=lambda x: x['score'])[:10]
print(f"\n" + "=" * 80)
print("BOTTOM 10 SCORING CVs:")
print("=" * 80)
for i, r in enumerate(bottom_10, 1):
    print(f"\n{i}. CV#{r['cv_id']} {r['cv_name']} vs {r['jd_title']}")
    print(f"   Score: {r['score']}/100")
    print(f"   Language: {r['cv_language']}")
    print(f"   Field: {r['cv_field']}")
    print(f"   Experience: {r['cv_experience_years']} years")

# Analyze by field
print(f"\n" + "=" * 80)
print("SCORE DISTRIBUTION BY FIELD:")
print("=" * 80)
field_scores = defaultdict(list)
for r in results:
    field_scores[r['cv_field']].append(r['score'])

for field, scores in sorted(field_scores.items()):
    avg = sum(scores) / len(scores)
    min_score = min(scores)
    max_score = max(scores)
    print(f"\n{field.upper()}:")
    print(f"  Average: {avg:.2f}")
    print(f"  Range: {min_score:.2f} - {max_score:.2f}")
    print(f"  Distribution: <50: {sum(1 for s in scores if s < 50)}, 50-60: {sum(1 for s in scores if 50 <= s < 60)}, 60-70: {sum(1 for s in scores if 60 <= s < 70)}, 70+: {sum(1 for s in scores if s >= 70)}")

# Calculate what would need to change to reach 90% average
print(f"\n" + "=" * 80)
print("PATH TO 90% AVERAGE:")
print("=" * 80)
current_avg = sum(scores) / len(scores)
target_avg = 90.0
needed_increase = target_avg - current_avg

print(f"Current average: {current_avg:.2f}")
print(f"Target average: {target_avg:.2f}")
print(f"Needed increase: +{needed_increase:.2f} points")
print(f"\nTo reach 90% average, all CVs would need to increase by {needed_increase:.2f} points on average")
print(f"This would require:")
print(f"  - Better keyword matching algorithms")
print(f"  - Weights adjustment (currently tech 40%, experience 20%, soft 15%)")
print(f"  - Contextual soft skills detection (e.g., 'led team' → leadership)")
print(f"  - Better experience matching (years + relevance)")
print(f"  - Achievement quantification detection")

# Analyze common weaknesses
print(f"\n" + "=" * 80)
print("SCORE CHARACTERISTICS:")
print("=" * 80)
print(f"Total CVs tested: {len(results)}")
print(f"CVs scoring  >= 70: {sum(1 for s in scores if s >= 70)} ({sum(1 for s in scores if s >=  70)/len(scores)*100:.1f}%)")
print(f"CVs scoring 60-70: {sum(1 for s in scores if 60 <= s < 70)} ({sum(1 for s in scores if 60 <= s < 70)/len(scores)*100:.1f}%)")
print(f"CVs scoring 50-60: {sum(1 for s in scores if 50 <= s < 60)} ({sum(1 for s in scores if 50 <= s < 60)/len(scores)*100:.1f}%)")
print(f"CVs scoring < 50: {sum(1 for s in scores if s < 50)} ({sum(1 for s in scores if s < 50)/len(scores)*100:.1f}%)")

print(f"\n" + "=" * 80)
print("RECOMMENDATIONS FOR REACHING 90%:")
print("=" * 80)
print("""
1. ADJUST SCORING WEIGHTS:
   - Current weights may be too strict
   - Consider partial credit for related skills (e.g., Vue.js counts for React knowledge)
   - Increase base scores for structural completeness
   
2. IMPLEMENT SYNONYM/RELATED SKILLS:
   - Node.js experience should boost Express score
   - PostgreSQL should count toward "SQL database" requirement
   - AWS should partially count toward "cloud" requirement
   
3. CONTEXTUAL SOFT SKILLS DETECTION:
   - "Led team of X" → leadership
   - "Collaborated with" → teamwork
   - "Presented to stakeholders" → communication
   - "Solved complex problems" → problem solving
   
4. SMARTER EXPERIENCE MATCHING:
   - Don't penalize too heavily for 1-2 year gaps
   - Consider total career length, not just current role
   - Weight recent experience higher
   
5. ACHIEVEMENT-BASED SCORING:
   - Bonus for quantified achievements (increased X by Y%)
   - Recognize impact indicators
   
6. NORMALIZE FOR FIELD DIFFERENCES:
   - Software/Data fields inherently have more specific tech requirements
   - Marketing/HR have more soft skill requirements
   - Adjust weights by field type

7. BASELINE ADJUSTMENT:
   - Set minimum score at 50 for any CV with basic structure
   - Scale scores: 50-100 instead of 0-100
   - This recognizes that even a weak CV has some value
""")
