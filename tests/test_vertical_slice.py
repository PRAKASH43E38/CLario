import pytest
from fastapi.testclient import TestClient

from app.db.session import create_tables
from app.main import app

create_tables()
client = TestClient(app)


def test_complete_vertical_learning_slice():
    # 1. Auth / Dev Login
    res_login = client.post(
        "/api/v1/auth/dev-login",
        json={"email": "verticalslice@clario.ai", "display_name": "Slice Learner"},
    )
    assert res_login.status_code == 200, res_login.text
    user_data = res_login.json()
    assert user_data["email"] == "verticalslice@clario.ai"

    # 2. Onboarding: Profile Setup
    res_prof = client.put(
        "/api/v1/onboarding/profile",
        json={
            "name": "Slice Learner",
            "age_range": "20-24",
            "education_level": "Undergraduate",
            "domain": "Computer Science",
            "prior_learning": "Basic Python",
        },
    )
    assert res_prof.status_code == 204

    # 3. Onboarding: Exactly 5 Mindset Questions Intake
    res_mindset = client.put(
        "/api/v1/onboarding/mindset",
        json={
            "answers": [
                {"question_number": 1, "answer": "A"},
                {"question_number": 2, "answer": "B"},
                {"question_number": 3, "answer": "C"},
                {"question_number": 4, "answer": "D"},
                {"question_number": 5, "answer": "A"},
            ]
        },
    )
    assert res_mindset.status_code == 204

    # 4. New Learning Session Input (Task, Goal, Learner State, Interests)
    res_session = client.post(
        "/api/v1/sessions",
        json={
            "task": "Learn Machine Learning Fundamentals",
            "goal": "Understand how linear regression predicts continuous values",
            "learner_state": "I know Python arrays but gradient descent formula is confusing",
            "interests": "Predicting house prices and sports analytics",
        },
    )
    assert res_session.status_code == 201
    session_id = res_session.json()["id"]

    # 5. Dynamic Roadmap Generation
    res_roadmap = client.post(f"/api/v1/sessions/{session_id}/roadmap")
    assert res_roadmap.status_code == 201
    roadmap_data = res_roadmap.json()
    assert "nodes" in roadmap_data
    assert len(roadmap_data["nodes"]) > 0

    first_node = roadmap_data["nodes"][0]
    roadmap_id = roadmap_data["id"]

    # 6. Get or Create Learning Activity for First Node
    res_act = client.post(f"/api/v1/roadmaps/{roadmap_id}/nodes/{first_node['id']}/activity")
    assert res_act.status_code == 201
    activity_data = res_act.json()
    assert "prompt" in activity_data
    activity_id = activity_data["id"]

    # 7. Submit Attempt for Activity (Testing evaluation & misconception logic)
    res_attempt = client.post(
        f"/api/v1/activities/{activity_id}/attempts",
        json={"response": "Linear regression fits a straight line y = wx + b to minimize error between predicted and actual values."},
    )
    assert res_attempt.status_code == 200
    attempt_data = res_attempt.json()
    assert "result" in attempt_data
    assert "clarity_awarded" in attempt_data
    assert "xp_awarded" in attempt_data

    # 8. User Stats Verification (XP, Clarity, Clarity Streak)
    res_stats = client.get("/api/v1/user/stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["xp"] >= 0
    assert stats["clarity"] >= 0
