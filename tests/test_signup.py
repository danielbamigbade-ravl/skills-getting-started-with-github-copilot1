"""Tests for the signup endpoint"""

import pytest


def test_signup_successful(client, fresh_activities, sample_activity, sample_email):
    """
    Arrange: Prepare a client, fresh activities, and test email
    Act: Make a POST request to signup endpoint with valid data
    Assert: Verify signup is successful and participant is added
    """
    # Arrange
    activity = sample_activity
    email = sample_email
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        method="POST"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity]["participants"]


def test_signup_activity_not_found(client, fresh_activities, sample_email):
    """
    Arrange: Prepare a client and sample email
    Act: Make a POST request to signup endpoint with non-existent activity
    Assert: Verify 404 error is returned
    """
    # Arrange
    non_existent_activity = "Nonexistent Activity"
    email = sample_email
    
    # Act
    response = client.post(
        f"/activities/{non_existent_activity}/signup?email={email}",
        method="POST"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email(client, fresh_activities, sample_activity):
    """
    Arrange: Prepare activity with existing participant
    Act: Try to signup with email already registered
    Assert: Verify 400 error for duplicate signup
    """
    # Arrange
    activity = sample_activity
    existing_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={existing_email}",
        method="POST"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_full_activity(client, fresh_activities, sample_email):
    """
    Arrange: Prepare an activity with limited spots that is now full
    Act: Try to signup for full activity (this test assumes we can fill it)
    Assert: Current implementation doesn't check max_participants on signup,
            but this documents expected behavior for future enhancement
    """
    # Note: Current implementation doesn't enforce max_participants limit
    # This test documents where that validation could be added
    activity = "Tennis Club"  # Has max 10, currently 1 participant
    email = sample_email
    
    # Current behavior: allows signup even if full
    # Future: should return error if max_participants reached
    response = client.post(
        f"/activities/{activity}/signup?email={email}",
        method="POST"
    )
    
    # Currently succeeds
    assert response.status_code == 200


def test_signup_special_characters_in_email(client, fresh_activities, sample_activity):
    """
    Arrange: Prepare to test email with URL-encoded characters
    Act: Make signup request with encoded email
    Assert: Verify special characters in email are handled correctly
    """
    # Arrange
    activity = sample_activity
    special_email = "test+student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={special_email}",
        method="POST"
    )
    
    # Assert
    assert response.status_code == 200
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert special_email in activities_data[activity]["participants"]


def test_signup_multiple_activities(client, fresh_activities, sample_email):
    """
    Arrange: Prepare test email and multiple activities
    Act: Signup same email to multiple activities
    Assert: Verify email can be in multiple activities
    """
    # Arrange
    email = sample_email
    activities_list = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    for activity in activities_list:
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            method="POST"
        )
        assert response.status_code == 200
    
    # Assert
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    for activity in activities_list:
        assert email in activities_data[activity]["participants"]
