from copy import deepcopy

from src.app import activities


def test_signup_adds_participant_to_selected_activity(client):
    # Arrange
    activity_name = "Chess Club"
    other_activity = "Programming Class"
    email = "new.student@mergington.edu"
    other_participants = deepcopy(activities[other_activity]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities[activity_name]["participants"]
    assert activities[other_activity]["participants"] == other_participants


def test_signup_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "new.student@mergington.edu"
    original_activities = deepcopy(activities)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activities == original_activities


def test_signup_duplicate_participant_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert activities[activity_name]["participants"].count(email) == 1


def test_signup_without_email_returns_validation_error(client):
    # Arrange
    activity_name = "Chess Club"
    original_participants = deepcopy(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
    assert activities[activity_name]["participants"] == original_participants