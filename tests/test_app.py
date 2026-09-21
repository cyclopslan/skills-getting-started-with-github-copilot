from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant_from_activity():
    activity_name = "Chess Club"
    email = "remove.me@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
