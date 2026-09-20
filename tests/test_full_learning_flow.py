from fastapi.testclient import TestClient

from app.db.session import create_tables
from app.main import app

create_tables()
client = TestClient(app)




def test_auth_and_onboarding_flow():
    # 1. Dev login
    res = client.post("/api/v1/auth/dev-login", json={"email": "testlearner@clario.ai", "display_name": "Test Learner"})
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["email"] == "testlearner@clario.ai"

    # 2. Check /auth/me
    res_me = client.get("/api/v1/auth/me")
    assert res_me.status_code == 200
    assert res_me.json()["id"] == data["id"]

    # 3. Save profile
    res_prof = client.put(
        "/api/v1/onboarding/profile",
        json={
            "name": "Test Learner",
            "age_range": "20-24",
            "education_level": "Undergraduate",
            "domain": "Computer Science",
            "prior_learning": "Basic Python",
        },
    )
    assert res_prof.status_code == 204

    # 4. Save 5 Mindset responses
    res_mindset = client.put(
        "/api/v1/onboarding/mindset",
        json={
            "answers": [
                {"question_number": 1, "answer": "A"},
                {"question_number": 2, "answer": "D"},
                {"question_number": 3, "answer": "A"},
                {"question_number": 4, "answer": "D"},
                {"question_number": 5, "answer": "A"},
            ]
        },
    )
    assert res_mindset.status_code == 204


def test_session_and_stats_flow():
    # Dev login
    client.post("/api/v1/auth/dev-login", json={"email": "testlearner@clario.ai", "display_name": "Test Learner"})

    # Create session
    res_session = client.post(
        "/api/v1/sessions",
        json={
            "task": "Learn Machine Learning Fundamentals",
            "goal": "Understand how model weights update through gradient descent",
            "learner_state": "I know basic Python and algebra but calculus feels tricky",
            "interests": "Robotics and gaming",
        },
    )
    assert res_session.status_code == 201
    session_data = res_session.json()
    assert "id" in session_data

    # User stats check
    res_stats = client.get("/api/v1/user/stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert "xp" in stats
    assert "clarity" in stats

    # Achievements check
    res_ach = client.get("/api/v1/user/achievements")
    assert res_ach.status_code == 200
    assert isinstance(res_ach.json(), list)

    # Insights check
    res_ins = client.get("/api/v1/user/insights")
    assert res_ins.status_code == 200
    assert isinstance(res_ins.json(), list)
