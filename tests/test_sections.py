"""
Tests for the sections endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a TestClient instance for the app."""
    with TestClient(app) as client:
        yield client


def test_generate_section_success(client):
    """Test POST /generate-section with valid request."""
    request_data = {
        "company_id": "123",
        "section_type": "innovation_description",
        "text": "AI automation SaaS application"
    }
    
    response = client.post("/generate-section", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "company_id" in data
    assert "section_type" in data
    assert "generated_text" in data
    assert "sources" in data
    assert "request_id" in data
    assert "created_at" in data
    
    # Check values
    assert data["company_id"] == "123"
    assert data["section_type"] == "innovation_description"
    assert isinstance(data["generated_text"], str)
    assert len(data["generated_text"]) > 0
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0


def test_generate_section_missing_field(client):
    """Test POST /generate-section with missing required field."""
    request_data = {
        "company_id": "123",
        "section_type": "innovation_description"
        # Missing 'text' field
    }
    
    response = client.post("/generate-section", json=request_data)
    
    # Should return 422 Unprocessable Entity for validation error
    assert response.status_code == 422


def test_generate_section_empty_text(client):
    """Test POST /generate-section with empty text field."""
    request_data = {
        "company_id": "123",
        "section_type": "innovation_description",
        "text": ""
    }
    
    response = client.post("/generate-section", json=request_data)
    
    # Empty text is still valid according to Pydantic (str type)
    # The endpoint should still process it
    assert response.status_code == 200


def test_history_after_generation(client):
    """Test GET /history/{company_id} after making a generation request."""
    # First, make a generation request
    request_data = {
        "company_id": "456",
        "section_type": "market_analysis",
        "text": "market trends and competition"
    }
    
    gen_response = client.post("/generate-section", json=request_data)
    assert gen_response.status_code == 200
    gen_data = gen_response.json()
    request_id = gen_data["request_id"]
    
    # Now get history for this company
    history_response = client.get(f"/history/{request_data['company_id']}")
    assert history_response.status_code == 200
    
    history_data = history_response.json()
    assert isinstance(history_data, list)
    assert len(history_data) > 0
    
    # Find our request in history
    found = False
    for entry in history_data:
        if entry["request_id"] == request_id:
            found = True
            assert entry["company_id"] == "456"
            assert entry["section_type"] == "market_analysis"
            assert "sources" in entry
            assert "created_at" in entry
            break
    
    assert found, "Generated request not found in history"


def test_history_empty_company(client):
    """Test GET /history/{company_id} for company with no history."""
    # Use a company ID that likely doesn't have history
    response = client.get("/history/nonexistent-company-999")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should be empty or contain no matching entries
    # (might not be empty if other tests ran first)


def test_root_endpoint(client):
    """Test GET / root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data

