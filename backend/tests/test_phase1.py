import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.services.seed import seed_database

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db, force_reset=True)
    db.close()
    yield

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"]["status"] == "connected"
    assert data["database"]["patient_count"] == 20
    assert data["database"]["doctor_count"] == 4
    assert data["database"]["room_count"] == 3

def test_get_doctors():
    response = client.get("/api/doctors")
    assert response.status_code == 200
    doctors = response.json()
    assert len(doctors) == 4
    names = [d["name"] for d in doctors]
    assert "Dr. Sarah Jenkins" in names
    for d in doctors:
        assert d["available_from"] == "09:00"
        assert d["available_until"] == "13:00"

def test_get_rooms():
    response = client.get("/api/rooms")
    assert response.status_code == 200
    rooms = response.json()
    assert len(rooms) == 3
    for r in rooms:
        assert r["available_from"] == "09:00"
        assert r["available_until"] == "13:00"

def test_get_patients():
    response = client.get("/api/patients")
    assert response.status_code == 200
    patients = response.json()
    assert len(patients) == 20

    # Verify priority levels distribution
    priorities = {p["priority"] for p in patients}
    assert priorities == {"HIGH", "MEDIUM", "LOW"}

    # Verify consultation durations (10 to 30 mins)
    for p in patients:
        assert 10 <= p["consultation_duration"] <= 30
        assert ":" in p["arrival_time"]

def test_patient_validation():
    # Test invalid duration < 10
    invalid_patient = {
        "name": "Invalid Patient",
        "arrival_time": "09:15",
        "priority": "HIGH",
        "consultation_duration": 5
    }
    response = client.post("/api/patients", json=invalid_patient)
    assert response.status_code == 422

    # Test invalid arrival time format
    invalid_time = {
        "name": "Invalid Patient 2",
        "arrival_time": "25:99",
        "priority": "MEDIUM",
        "consultation_duration": 20
    }
    response2 = client.post("/api/patients", json=invalid_time)
    assert response2.status_code == 422

def test_delete_patient():
    # Create a temporary patient to delete
    create_res = client.post("/api/patients", json={
        "name": "Temp Deletable Patient",
        "arrival_time": "10:00",
        "priority": "LOW",
        "consultation_duration": 15
    })
    assert create_res.status_code == 201
    p_id = create_res.json()["id"]

    # Delete the patient
    del_res = client.delete(f"/api/patients/{p_id}")
    assert del_res.status_code == 204

    # Verify patient is gone
    get_res = client.get(f"/api/patients/{p_id}")
    assert get_res.status_code == 404

def test_delete_doctor():
    create_res = client.post("/api/doctors", json={
        "name": "Dr. Temporary",
        "available_from": "09:00",
        "available_until": "13:00"
    })
    assert create_res.status_code == 201
    d_id = create_res.json()["id"]

    del_res = client.delete(f"/api/doctors/{d_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/doctors/{d_id}")
    assert get_res.status_code == 404

def test_delete_room():
    create_res = client.post("/api/rooms", json={
        "name": "Temporary Room",
        "available_from": "09:00",
        "available_until": "13:00"
    })
    assert create_res.status_code == 201
    r_id = create_res.json()["id"]

    del_res = client.delete(f"/api/rooms/{r_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/rooms/{r_id}")
    assert get_res.status_code == 404

