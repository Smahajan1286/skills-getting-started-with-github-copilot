from copy import deepcopy

from src.app import activities


def test_unregister_removes_selected_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    remaining_participant = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]
    assert remaining_participant in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    original_activities = deepcopy(activities)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activities == original_activities


def test_unregister_unknown_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    original_participants = deepcopy(activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
    assert activities[activity_name]["participants"] == original_participants


def test_unregister_without_email_returns_validation_error(client):
    # Arrange
    activity_name = "Chess Club"
    original_participants = deepcopy(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants")

    # Assert
    assert response.status_code == 422
    assert activities[activity_name]["participants"] == original_participants