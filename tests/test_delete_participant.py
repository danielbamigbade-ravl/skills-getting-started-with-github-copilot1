"""Tests for the delete participant endpoint"""

import pytest


def test_delete_participant_successful(client, fresh_activities, sample_activity):
    """
    Arrange: Prepare activity with known participants
    Act: Make a DELETE request to remove a participant
    Assert: Verify participant is removed successfully
    """
    # Arrange
    activity = sample_activity
    email = "michael@mergington.edu"  # Existing participant in Chess Club
    
    # Verify participant exists before deletion
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity]["participants"]
    initial_count = len(activities_data[activity]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity]["participants"]
    assert len(activities_data[activity]["participants"]) == initial_count - 1


def test_delete_participant_activity_not_found(client, fresh_activities, sample_email):
    """
    Arrange: Prepare non-existent activity
    Act: Make a DELETE request for non-existent activity
    Assert: Verify 404 error is returned
    """
    # Arrange
    non_existent_activity = "Nonexistent Activity"
    email = sample_email
    
    # Act
    response = client.delete(
        f"/activities/{non_existent_activity}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_delete_participant_not_in_activity(client, fresh_activities, sample_activity, sample_email):
    """
    Arrange: Prepare activity and email not in that activity's participants
    Act: Make a DELETE request for non-existent participant
    Assert: Verify 404 error is returned
    """
    # Arrange
    activity = sample_activity
    email = sample_email  # Not in any activity initially
    
    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]


def test_delete_multiple_participants(client, fresh_activities, sample_activity):
    """
    Arrange: Prepare activity with multiple participants
    Act: Delete each participant one by one
    Assert: Verify all are removed successfully
    """
    # Arrange
    activity = sample_activity
    participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Verify both are in activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert len(activities_data[activity]["participants"]) == 2
    
    # Act & Assert for each participant
    for email in participants:
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )
        assert response.status_code == 200
    
    # Verify all are removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert len(activities_data[activity]["participants"]) == 0


def test_delete_same_participant_twice(client, fresh_activities, sample_activity):
    """
    Arrange: Prepare to delete a participant
    Act: Delete participant, then try to delete same participant again
    Assert: First succeeds, second fails with 404
    """
    # Arrange
    activity = sample_activity
    email = "michael@mergington.edu"
    
    # Act - First deletion
    response1 = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    assert response1.status_code == 200
    
    # Act - Second deletion attempt
    response2 = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    # Assert
    assert response2.status_code == 404
    data = response2.json()
    assert "Participant not found" in data["detail"]


def test_delete_participant_with_special_characters(client, fresh_activities, sample_activity):
    """
    Arrange: Sign up a participant with special characters, then delete
    Act: Make DELETE request with special characters in email
    Assert: Verify special characters are handled correctly
    """
    # Arrange
    activity = sample_activity
    special_email = "test+special@mergington.edu"
    
    # First signup the participant
    signup_response = client.post(
        f"/activities/{activity}/signup?email={special_email}",
        method="POST"
    )
    assert signup_response.status_code == 200
    
    # Act
    response = client.delete(
        f"/activities/{activity}/participants/{special_email}"
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert special_email not in activities_data[activity]["participants"]
