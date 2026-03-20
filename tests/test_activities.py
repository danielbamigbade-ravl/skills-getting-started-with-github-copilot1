"""Tests for the /activities endpoint"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    Arrange: Set up fresh activities
    Act: Make a GET request to /activities
    Assert: Verify response contains all activities with correct structure
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify we get a dictionary with activity names as keys
    assert isinstance(data, dict)
    assert len(data) == 9
    
    # Verify required activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_includes_correct_structure(client, fresh_activities):
    """
    Arrange: Set up fresh activities
    Act: Make a GET request to /activities
    Assert: Verify each activity has all required fields
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure for one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Verify participants is a list
    assert isinstance(chess_club["participants"], list)


def test_get_activities_includes_participant_data(client, fresh_activities):
    """
    Arrange: Set up fresh activities with known participants
    Act: Make a GET request to /activities
    Assert: Verify participant data is correctly returned
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Chess Club should have specific participants
    chess_club = data["Chess Club"]
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]
    assert len(chess_club["participants"]) == 2


def test_get_activities_activity_details(client, fresh_activities):
    """
    Arrange: Set up fresh activities
    Act: Make a GET request to /activities
    Assert: Verify specific activity details are correct
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    programming = data["Programming Class"]
    assert programming["description"] == "Learn programming fundamentals and build software projects"
    assert programming["schedule"] == "Tuesdays and Thursdays, 3:30 PM - 4:30 PM"
    assert programming["max_participants"] == 20
