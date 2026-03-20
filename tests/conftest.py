"""Shared pytest fixtures for API tests"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Reset activities to a known state before each test.
    This ensures test isolation by providing a fresh copy of activities data.
    """
    original_activities = activities.copy()
    
    # Reset activities to initial state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and gameplay",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and participate in matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "ava@mergington.edu"]
        },
        "Drama Club": {
            "description": "Performing arts including theater and improv",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["james@mergington.edu", "ryan@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore experiments and scientific inquiry",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["nina@mergington.edu"]
        }
    })
    
    yield activities
    
    # Cleanup: restore original state
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activity():
    """Provide a known activity name for tests"""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Provide a test email for signup tests"""
    return "test.student@mergington.edu"
