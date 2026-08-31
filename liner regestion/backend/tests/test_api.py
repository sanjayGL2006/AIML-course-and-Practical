import os
import json
import pytest
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test GET /api/health returns 200 and expected status."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['message'] == 'API is running'

def test_valid_prediction(client):
    """Test POST /api/predict with valid height 170 cm."""
    response = client.post('/api/predict', json={'height': 170})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['height'] == 170
    assert 'predicted_weight' in data
    assert isinstance(data['predicted_weight'], float)
    assert data['predicted_weight'] == 65.42

def test_missing_height(client):
    """Test POST /api/predict with missing height field."""
    response = client.post('/api/predict', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'Please enter your height' in data['error']

def test_invalid_string_height(client):
    """Test POST /api/predict with non-numeric string."""
    response = client.post('/api/predict', json={'height': 'abc'})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'Please enter a valid height' in data['error']

def test_negative_height(client):
    """Test POST /api/predict with negative height."""
    response = client.post('/api/predict', json={'height': -170})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_zero_height(client):
    """Test POST /api/predict with zero height."""
    response = client.post('/api/predict', json={'height': 0})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_out_of_range_height(client):
    """Test POST /api/predict with height out of allowed range (50-250 cm)."""
    response = client.post('/api/predict', json={'height': 300})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'between 50 cm and 250 cm' in data['error']
