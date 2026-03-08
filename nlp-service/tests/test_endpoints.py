import pytest
import requests
import time

BASE_URL = "http://localhost:8001"

def test_health_endpoint():
    """Test that the health endpoint is responding"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_score_cv_english():
    """Test CV scoring with English language using BERT"""
    payload = {
        "cv_text": "Senior Software Engineer with 5+ years of experience in Python, Django, Docker, Kubernetes, AWS",
        "jd_text": "Looking for a Python developer with cloud experience",
        "language": "en"
    }
    response = requests.post(f"{BASE_URL}/score-cv", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "score" in data["data"]
    assert data["data"]["score"] >= 0
    assert data["data"]["score"] <= 100

def test_score_cv_vietnamese():
    """Test CV scoring with Vietnamese language using PhoBERT"""
    payload = {
        "cv_text": "Kỹ sư phần mềm với 3 năm kinh nghiệm Python, Django, Docker",
        "jd_text": "Tìm kiếm lập trình viên Python có kinh nghiệm",
        "language": "vi"
    }
    response = requests.post(f"{BASE_URL}/score-cv", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "score" in data["data"]

def test_ner_english():
    """Test English NER with BERT"""
    payload = {
        "text": "I have 5 years of experience with Python, JavaScript, React, and Docker. Expert in AWS and Kubernetes."
    }
    response = requests.post(f"{BASE_URL}/ner/en", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "entities" in data["data"]
    assert data["data"]["model"] == "bert"
    
    # Check that some skills were detected
    skills = [e for e in data["data"]["entities"] if e["label"] == "SKILL"]
    assert len(skills) > 0

def test_ner_vietnamese():
    """Test Vietnamese NER with PhoBERT"""
    payload = {
        "text": "Tôi có 3 năm kinh nghiệm với Python, Django, và Docker"
    }
    response = requests.post(f"{BASE_URL}/ner/vi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "entities" in data["data"]
    assert data["data"]["model"] == "phobert"

def test_similarity():
    """Test semantic similarity with sentence-transformers"""
    payload = {
        "left_text": "I am a software engineer with Python experience",
        "right_text": "I am a developer skilled in Python programming"
    }
    response = requests.post(f"{BASE_URL}/similarity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "score" in data["data"]
    assert data["data"]["model"] == "sentence-transformers"
    # Similar sentences should have high similarity
    assert data["data"]["score"] > 0.7

def test_similarity_dissimilar():
    """Test similarity with very different texts"""
    payload = {
        "left_text": "I love cooking Italian food",
        "right_text": "Machine learning algorithms require large datasets"
    }
    response = requests.post(f"{BASE_URL}/similarity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    # Different sentences should have lower similarity
    assert data["data"]["score"] < 0.5

def test_performance_ner():
    """Basic performance test for NER endpoint"""
    payload = {
        "text": "Software engineer with 5 years experience in Python, Java, Docker, Kubernetes, AWS, React, Node.js"
    }
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/ner/en", json=payload)
    elapsed = time.time() - start
    
    assert response.status_code == 200
    # NER should complete within 3 seconds
    assert elapsed < 3.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
