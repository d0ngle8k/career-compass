"""
Batch test CV scoring with 100 CVs and analyze results
"""
import asyncio
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import aiohttp
import statistics

# Fix Windows console encoding for Vietnamese characters
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

NLP_SERVICE_URL = "http://127.0.0.1:8001"

async def score_cv(session: aiohttp.ClientSession, cv_text: str, jd_text: str) -> Dict:
    """Score a single CV against a JD"""
    url = f"{NLP_SERVICE_URL}/score-cv"
    payload = {
        "cv_text": cv_text,
        "jd_text": jd_text
    }
    
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                result = await response.json()
                # Handle envelope response
                if "data" in result and result.get("success"):
                    return result["data"]
                elif "success" in result and not result.get("success"):
                    return {"error": result.get ("error", "Unknown error"), "score": 0}
                else:
                    return result
            else:
                return {"error": f"HTTP {response.status}", "score": 0}
    except Exception as e:
        return {"error": str(e), "score": 0}

async def ner_extract(session: aiohttp.ClientSession, text: str, language: str) -> Dict:
    """Extract named entities from text"""
    endpoint = "ner/vi" if language == "vi" else "ner/en"
    url = f"{NLP_SERVICE_URL}/{endpoint}"
    payload = {"text": text}
    
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": f"HTTP {response.status}", "entities": []}
    except Exception as e:
        return {"error": str(e), "entities": []}

async def batch_test_scoring(cv_dir: Path, jd_dir: Path, output_file: Path, max_tests: int = 100):
    """Batch test CV scoring"""
    
    # Load CV metadata
    with open(cv_dir / "metadata.json", "r", encoding="utf-8") as f:
        cv_metadata = json.load(f)
    
    # Load JD metadata
    with open(jd_dir / "metadata.json", "r", encoding="utf-8") as f:
        jd_metadata = json.load(f)
    
    # Create test cases: match CVs with relevant JDs (same field and language)
    test_cases = []
    for cv_info in cv_metadata["cvs"][:max_tests]:
        # Find matching JD (same field and language)
        matching_jds = [
            jd for jd in jd_metadata["jds"]
            if jd["field"] == cv_info["field"] and jd["language"] == cv_info["language"]
        ]
        
        if matching_jds:
            jd_info = matching_jds[0]  # Take first matching JD
            
            # Load CV text
            cv_path = cv_dir / cv_info["filename"]
            with open(cv_path, "r", encoding="utf-8") as f:
                cv_text = f.read()
            
            # Load JD text
            jd_path = jd_dir / jd_info["filename"]
            with open(jd_path, "r", encoding="utf-8") as f:
                jd_text = f.read()
            
            test_cases.append({
                "cv_info": cv_info,
                "jd_info": jd_info,
                "cv_text": cv_text,
                "jd_text": jd_text
            })
    
    print(f"Created {len(test_cases)} test cases")
    print(f"Testing CV scoring and NER extraction...")
    
    results = []
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Test scoring performance
        for i, test_case in enumerate(test_cases, 1):
            print(f"Testing {i}/{len(test_cases)}: {test_case['cv_info']['name']} vs {test_case['jd_info']['title']}")
            
            test_start = time.time()
            
            # Score CV
            score_result = await score_cv(session, test_case["cv_text"], test_case["jd_text"])
            score_time = time.time() - test_start
            
            # Extract NER from CV
            ner_start = time.time()
            ner_result = await ner_extract(
                session,
                test_case["cv_text"],
                test_case["cv_info"]["language"]
            )
            ner_time = time.time() - ner_start
            
            result = {
                "cv_id": test_case["cv_info"]["id"],
                "cv_name": test_case["cv_info"]["name"],
                "cv_field": test_case["cv_info"]["field"],
                "cv_language": test_case["cv_info"]["language"],
                "cv_experience_years": test_case["cv_info"]["experience_years"],
                "jd_id": test_case["jd_info"]["id"],
                "jd_title": test_case["jd_info"]["title"],
                "jd_field": test_case["jd_info"]["field"],
                "score": score_result.get("score", 0),
                "score_breakdown": score_result.get("breakdown", {}),
                "score_time": score_time,
                "score_error": score_result.get("error"),
                "ner_entities": ner_result.get("entities", []),
                "ner_time": ner_time,
                "ner_error": ner_result.get("error"),
                "total_time": score_time + ner_time
            }
            
            results.append(result)
            
            # Print progress
            if i % 10 == 0:
                avg_time = statistics.mean([r["total_time"] for r in results])
                print(f"  Progress: {i}/{len(test_cases)} | Avg time: {avg_time:.2f}s")
    
    total_time = time.time() - start_time
    
    # Analyze results
    analysis = analyze_results(results, total_time)
    
    # Save results
    output_data = {
        "test_info": {
            "total_tests": len(test_cases),
            "total_time": total_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "results": results,
        "analysis": analysis
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Batch testing complete!")
    print(f"   Total tests: {len(test_cases)}")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Results saved to: {output_file}")
    
    # Print analysis summary
    print_analysis(analysis)
    
    return output_data

def analyze_results(results: List[Dict], total_time: float) -> Dict:
    """Analyze test results"""
    
    # Basic statistics
    scores = [r["score"] for r in results if r.get("score") is not None]
    score_times = [r["score_time"] for r in results]
    ner_times = [r["ner_time"] for r in results]
    
    # Errors
    score_errors = [r for r in results if r.get("score_error")]
    ner_errors = [r for r in results if r.get("ner_error")]
    
    # By language
    vi_results = [r for r in results if r["cv_language"] == "vi"]
    en_results = [r for r in results if r["cv_language"] == "en"]
    
    vi_scores = [r["score"] for r in vi_results if r.get("score") is not None]
    en_scores = [r["score"] for r in en_results if r.get("score") is not None]
    
    # By field
    field_stats = {}
    for field in ["software", "data", "marketing", "finance", "hr"]:
        field_results = [r for r in results if r["cv_field"] == field]
        if field_results:
            field_scores = [r["score"] for r in field_results if r.get("score") is not None]
            field_stats[field] = {
                "count": len(field_results),
                "avg_score": statistics.mean(field_scores) if field_scores else 0,
                "min_score": min(field_scores) if field_scores else 0,
                "max_score": max(field_scores) if field_scores else 0,
                "avg_entities": statistics.mean([len(r.get("ner_entities", [])) for r in field_results]) if field_results else 0
            }
    
    # NER entity types distribution
    entity_types = {}
    for result in results:
        for entity in result.get("ner_entities", []):
            entity_type = entity.get("entity_group", entity.get("label", "UNKNOWN"))
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
    
    analysis = {
        "overall": {
            "total_tests": len(results),
            "total_time": total_time,
            "avg_time_per_test": total_time / len(results) if results else 0,
            "success_rate": (len(results) - len(score_errors)) / len(results) * 100 if results else 0
        },
        "scoring": {
            "avg_score": statistics.mean(scores) if scores else 0,
            "median_score": statistics.median(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "std_dev": statistics.stdev(scores) if len(scores) > 1 else 0,
            "avg_time": statistics.mean(score_times) if score_times else 0,
            "error_count": len(score_errors),
            "error_rate": len(score_errors) / len(results) * 100 if results else 0
        },
        "ner": {
            "total_entities_extracted": sum(len(r.get("ner_entities", [])) for r in results),
            "avg_entities_per_cv": statistics.mean([len(r.get("ner_entities", [])) for r in results]) if results else 0,
            "entity_types_distribution": entity_types,
            "avg_time": statistics.mean(ner_times) if ner_times else 0,
            "error_count": len(ner_errors),
            "error_rate": len(ner_errors) / len(results) * 100 if results else 0
        },
        "by_language": {
            "vietnamese": {
                "count": len(vi_results),
                "avg_score": statistics.mean(vi_scores) if vi_scores else 0,
                "avg_entities": statistics.mean([len(r.get("ner_entities", [])) for r in vi_results]) if vi_results else 0
            },
            "english": {
                "count": len(en_results),
                "avg_score": statistics.mean(en_scores) if en_scores else 0,
                "avg_entities": statistics.mean([len(r.get("ner_entities", [])) for r in en_results]) if en_results else 0
            }
        },
        "by_field": field_stats,
        "performance_issues": identify_performance_issues(results)
    }
    
    return analysis

def identify_performance_issues(results: List[Dict]) -> Dict:
    """Identify potential performance issues"""
    issues = {
        "low_scores": [],
        "high_variance_fields": [],
        "slow_operations": [],
        "ner_failures": []
    }
    
    # Low scores (< 30)
    for r in results:
        if r.get("score", 0) < 30:
            issues["low_scores"].append({
                "cv_name": r["cv_name"],
                "jd_title": r["jd_title"],
                "score": r["score"],
                "field": r["cv_field"]
            })
    
    # Slow operations (> 5 seconds)
    for r in results:
        if r.get("total_time", 0) > 5:
            issues["slow_operations"].append({
                "cv_name": r["cv_name"],
                "total_time": r["total_time"],
                "score_time": r["score_time"],
                "ner_time": r["ner_time"]
            })
    
    # NER failures (0 entities extracted)
    for r in results:
        if len(r.get("ner_entities", [])) == 0:
            issues["ner_failures"].append({
                "cv_name": r["cv_name"],
                "language": r["cv_language"],
                "error": r.get("ner_error")
            })
    
    # Field variance
    field_scores = {}
    for r in results:
        field = r["cv_field"]
        if field not in field_scores:
            field_scores[field] = []
        if r.get("score") is not None:
            field_scores[field].append(r["score"])
    
    for field, scores in field_scores.items():
        if len(scores) > 1:
            std_dev = statistics.stdev(scores)
            if std_dev > 20:  # High variance threshold
                issues["high_variance_fields"].append({
                    "field": field,
                    "std_dev": std_dev,
                    "avg_score": statistics.mean(scores)
                })
    
    return issues

def print_analysis(analysis: Dict):
    """Pretty print analysis results"""
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    print("\n[OVERALL] Performance:")
    print(f"   Total tests: {analysis['overall']['total_tests']}")
    print(f"   Total time: {analysis['overall']['total_time']:.2f}s")
    print(f"   Avg time per test: {analysis['overall']['avg_time_per_test']:.2f}s")
    print(f"   Success rate: {analysis['overall']['success_rate']:.1f}%")
    
    print("\n[SCORING] Statistics:")
    print(f"   Average score: {analysis['scoring']['avg_score']:.2f}")
    print(f"   Median score: {analysis['scoring']['median_score']:.2f}")
    print(f"   Score range: {analysis['scoring']['min_score']:.2f} - {analysis['scoring']['max_score']:.2f}")
    print(f"   Std deviation: {analysis['scoring']['std_dev']:.2f}")
    print(f"   Avg scoring time: {analysis['scoring']['avg_time']:.3f}s")
    print(f"   Error rate: {analysis['scoring']['error_rate']:.1f}%")
    
    print("\n[NER] Statistics:")
    print(f"   Total entities: {analysis['ner']['total_entities_extracted']}")
    print(f"   Avg entities per CV: {analysis['ner']['avg_entities_per_cv']:.1f}")
    print(f"   Avg NER time: {analysis['ner']['avg_time']:.3f}s")
    print(f"   Error rate: {analysis['ner']['error_rate']:.1f}%")
    
    print("\n[LANGUAGE] By Language:")
    print(f"   Vietnamese: {analysis['by_language']['vietnamese']['count']} CVs, "
          f"avg score: {analysis['by_language']['vietnamese']['avg_score']:.2f}, "
          f"avg entities: {analysis['by_language']['vietnamese']['avg_entities']:.1f}")
    print(f"   English: {analysis['by_language']['english']['count']} CVs, "
          f"avg score: {analysis['by_language']['english']['avg_score']:.2f}, "
          f"avg entities: {analysis['by_language']['english']['avg_entities']:.1f}")
    
    print("\n[FIELD] By Field:")
    for field, stats in analysis['by_field'].items():
        print(f"   {field}: {stats['count']} CVs, "
              f"avg score: {stats['avg_score']:.2f} ({stats['min_score']:.2f}-{stats['max_score']:.2f}), "
              f"avg entities: {stats['avg_entities']:.1f}")
    
    print("\n[ISSUES] Performance Issues:")
    issues = analysis['performance_issues']
    print(f"   Low scores (< 30): {len(issues['low_scores'])}")
    print(f"   Slow operations (> 5s): {len(issues['slow_operations'])}")
    print(f"   NER failures: {len(issues['ner_failures'])}")
    print(f"   High variance fields: {len(issues['high_variance_fields'])}")
    
    if issues['low_scores']:
        print("\n   Top 5 low scores:")
        for item in sorted(issues['low_scores'], key=lambda x: x['score'])[:5]:
            print(f"      - {item['cv_name']} vs {item['jd_title']}: {item['score']:.2f}")
    
    print("\n" + "="*80)

async def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent / "test_data"
    cv_dir = base_dir / "cvs"
    jd_dir = base_dir / "jds"
    output_file = base_dir / "scoring_test_results.json"
    
    # Check if NLP service is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NLP_SERVICE_URL}/health") as response:
                if response.status != 200:
                    print("❌ NLP service is not healthy!")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to NLP service: {e}")
        print(f"   Make sure NLP service is running on {NLP_SERVICE_URL}")
        return
    
    print(f"[OK] NLP service is running on {NLP_SERVICE_URL}")
    
    # Run batch testing
    await batch_test_scoring(cv_dir, jd_dir, output_file, max_tests=100)

if __name__ == "__main__":
    asyncio.run(main())
