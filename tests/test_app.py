import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import app as app_module


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app_module.app)

    response = client.delete(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]


def test_unregister_participant_returns_error_for_non_participant():
    client = TestClient(app_module.app)

    response = client.delete(
        "/activities/Chess%20Club/signup?email=not-a-student@example.com"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
