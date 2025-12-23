"""
Backend tests
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "healthy"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data

def test_get_diseases():
    """Test diseases list endpoint"""
    response = client.get("/api/diseases")
    assert response.status_code == 200
    data = response.json()
    assert "diseases" in data
    assert len(data["diseases"]) > 0

def test_get_symptom_types():
    """Test symptom types endpoint"""
    response = client.get("/api/symptoms/types")
    assert response.status_code == 200
    data = response.json()
    assert "types" in data
    assert len(data["types"]) > 0

def test_get_contact_info():
    """Test contact info endpoint"""
    response = client.get("/api/contact")
    assert response.status_code == 200
    data = response.json()
    assert "eitaa" in data
    assert "phone" in data

def test_invalid_disease():
    """Test invalid disease returns 404"""
    response = client.get("/api/videos/invalid_disease")
    assert response.status_code == 404

def test_save_symptom_invalid_user_id():
    """Test saving symptom with invalid user_id"""
    response = client.post("/api/symptoms", json={
        "user_id": "invalid",
        "symptom_type": "قند ناشتا",
        "value": "100"
    })
    assert response.status_code == 422

def test_save_symptom_invalid_type():
    """Test saving symptom with invalid type"""
    response = client.post("/api/symptoms", json={
        "user_id": "user_test123",
        "symptom_type": "invalid_type",
        "value": "100"
    })
    assert response.status_code == 422

def test_save_symptom_invalid_value():
    """Test saving symptom with invalid value"""
    response = client.post("/api/symptoms", json={
        "user_id": "user_test123",
        "symptom_type": "قند ناشتا",
        "value": "999"
    })
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting"""
    # این تست باید تعداد زیادی request بفرستد
    # برای اینکه rate limit trigger شود
    pass
