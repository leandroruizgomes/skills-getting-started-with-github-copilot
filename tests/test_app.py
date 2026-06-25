from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_remove_participant_from_activity():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]

    try:
        email = original_participants[0]
        response = client.delete(
            f"/activities/{quote(activity_name)}/participants/{quote(email)}"
        )

        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_remove_unknown_participant_returns_not_found():
    activity_name = "Chess Club"
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/unknown@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
