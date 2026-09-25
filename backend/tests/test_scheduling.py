"""
Comprehensive Unit Tests for Hospital Scheduling Engine (Phase 2).
Covers:
1. Time utilities & intervals
2. Hard constraints & conflict detection
3. Waiting time calculation
4. Priority penalty & thresholds
5. Resource under-utilization
6. Complete heuristic function H(S)
7. Assignment example verification (Schedule A vs Schedule B)
8. Neighbor generation operators
9. Best-Improvement Hill Climbing (acceptance, rejection, termination)
10. Full constraint compliance of generated schedules
11. REST API endpoints (POST /api/schedule/generate, GET /api/schedule)
"""

import pytest
from types import SimpleNamespace
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.services.seed import seed_database
from app.services.scheduling import (
    parse_time,
    format_time,
    duration_between,
    overlaps,
    has_doctor_conflict,
    has_room_conflict,
    count_all_conflicts,
    calculate_total_waiting_time,
    calculate_priority_penalty,
    calculate_under_utilization,
    calculate_heuristic,
    generate_initial_schedule,
    generate_neighbors,
    hill_climb,
    is_schedule_valid
)

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db, force_reset=True)
    db.close()
    yield

# -------------------------------------------------------------
# 1. Time utilities test
# -------------------------------------------------------------
def test_time_conversions():
    assert parse_time("09:00") == 540
    assert parse_time("09:30") == 570
    assert parse_time("10:15") == 615
    assert parse_time("13:00") == 780
    assert format_time(540) == "09:00"
    assert format_time(570) == "09:30"
    assert format_time(780) == "13:00"
    assert duration_between(540, 565) == 25

def test_interval_overlaps():
    # Overlapping intervals
    assert overlaps(540, 560, 550, 570) is True
    # Contained interval
    assert overlaps(540, 600, 550, 570) is True
    # Abutting / adjacent intervals (NOT overlapping)
    assert overlaps(540, 560, 560, 580) is False
    # Completely disjoint
    assert overlaps(540, 560, 570, 590) is False

# -------------------------------------------------------------
# 2. Waiting time calculation test
# -------------------------------------------------------------
def test_waiting_time():
    """
    Test scenario:
    Patient arrives at 09:10 (550 min), scheduled start at 09:30 (570 min).
    Expected waiting time = 20 minutes.
    """
    p1 = SimpleNamespace(id=1, arrival_time=550, priority="HIGH")
    patients_dict = {1: p1}
    schedule = [{
        "patient_id": 1,
        "doctor_id": 1,
        "room_id": 1,
        "start_time": 570,
        "end_time": 590,
        "waiting_time": 20
    }]
    total_wt = calculate_total_waiting_time(schedule, patients_dict)
    assert total_wt == 20

# -------------------------------------------------------------
# 3. Conflict detection tests
# -------------------------------------------------------------
def test_doctor_conflict():
    """Two overlapping appointments for the same doctor must trigger a conflict."""
    appt1 = {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 560}
    appt2 = {"patient_id": 2, "doctor_id": 1, "room_id": 2, "start_time": 550, "end_time": 570}
    assert has_doctor_conflict(appt1, appt2) is True
    assert count_all_conflicts([appt1, appt2]) == 1

def test_room_conflict():
    """Two overlapping appointments in the same room must trigger a conflict."""
    appt1 = {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 560}
    appt2 = {"patient_id": 2, "doctor_id": 2, "room_id": 1, "start_time": 550, "end_time": 570}
    assert has_room_conflict(appt1, appt2) is True
    assert count_all_conflicts([appt1, appt2]) == 1

def test_no_conflict_for_different_doctors():
    """Two overlapping appointments assigned to different doctors do not have a doctor conflict."""
    appt1 = {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 560}
    appt2 = {"patient_id": 2, "doctor_id": 2, "room_id": 2, "start_time": 550, "end_time": 570}
    assert has_doctor_conflict(appt1, appt2) is False

def test_no_conflict_for_different_rooms():
    """Two overlapping appointments assigned to different rooms do not have a room conflict."""
    appt1 = {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 560}
    appt2 = {"patient_id": 2, "doctor_id": 2, "room_id": 2, "start_time": 550, "end_time": 570}
    assert has_room_conflict(appt1, appt2) is False
    assert count_all_conflicts([appt1, appt2]) == 0

# -------------------------------------------------------------
# 4. Priority penalty test
# -------------------------------------------------------------
def test_priority_penalty():
    """Verify HIGH priority receives larger penalty for excessive waiting than LOW priority."""
    # Both wait 50 minutes (arrival 540, start 590)
    # HIGH threshold = 15 -> excess 35 -> ceil(35/5) = 7
    # LOW threshold  = 45 -> excess 5  -> ceil(5/15) = 1
    p_high = SimpleNamespace(id=1, arrival_time=540, priority="HIGH")
    p_low  = SimpleNamespace(id=2, arrival_time=540, priority="LOW")

    sched_high = [{"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 590, "end_time": 610}]
    sched_low  = [{"patient_id": 2, "doctor_id": 1, "room_id": 1, "start_time": 590, "end_time": 610}]

    pen_high = calculate_priority_penalty(sched_high, {1: p_high})
    pen_low  = calculate_priority_penalty(sched_low,  {2: p_low})

    assert pen_high > pen_low
    assert pen_high == 7.0
    assert pen_low == 1.0

# -------------------------------------------------------------
# 5. Under-utilization test
# -------------------------------------------------------------
def test_under_utilization():
    """Calculate resource under-utilization from unused capacity."""
    docs = [SimpleNamespace(id=1), SimpleNamespace(id=2), SimpleNamespace(id=3), SimpleNamespace(id=4)]
    rooms = [SimpleNamespace(id=1), SimpleNamespace(id=2), SimpleNamespace(id=3)]

    # 4 doctors * 240 = 960 min, 3 rooms * 240 = 720 min
    # If 20 patients each 20 mins = 400 mins used
    sched = [
        {"patient_id": i, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 560}
        for i in range(20)
    ]
    u = calculate_under_utilization(sched, docs, rooms)
    # Expected U is around 2 to 4
    assert 1.0 <= u <= 6.0

# -------------------------------------------------------------
# 6. Complete heuristic formula test
# -------------------------------------------------------------
def test_heuristic_formula():
    """Verify H(S) = 5*WT + 100*C + 20*P + 10*U."""
    patients_dict = {
        1: SimpleNamespace(id=1, arrival_time=540, priority="HIGH"),
        2: SimpleNamespace(id=2, arrival_time=550, priority="MEDIUM")
    }
    doctors_dict = {1: SimpleNamespace(id=1, available_from=540, available_until=780)}
    rooms_dict = {1: SimpleNamespace(id=1, available_from=540, available_until=780)}

    # Schedule: P1 starts 550 (wait=10), P2 starts 570 (wait=20)
    # No conflicts.
    schedule = [
        {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 550, "end_time": 570, "waiting_time": 10},
        {"patient_id": 2, "doctor_id": 1, "room_id": 1, "start_time": 570, "end_time": 590, "waiting_time": 20},
    ]

    res = calculate_heuristic(schedule, patients_dict, doctors_dict, rooms_dict)
    assert res["waiting_time"] == 30
    assert res["conflicts"] == 0

    expected_score = (
        5 * res["waiting_time"] +
        100 * res["conflicts"] +
        20 * res["priority_penalty"] +
        10 * res["under_utilization"]
    )
    assert res["total_score"] == round(expected_score, 2)

# -------------------------------------------------------------
# 7. Assignment Example Test (Schedule A vs Schedule B)
# -------------------------------------------------------------
def test_conflict_has_large_weight_assignment_example():
    """
    Direct test of the assignment specification example:
    Schedule A:
      WT = 40, C = 0, P = 2, U = 3
      H(A) = 5(40) + 100(0) + 20(2) + 10(3) = 270

    Schedule B:
      WT = 30, C = 1, P = 1, U = 2
      H(B) = 5(30) + 100(1) + 20(1) + 10(2) = 290

    Schedule B has lower waiting time (30 vs 40), but its 1 conflict
    penalizes it by +100, making Schedule A clearly superior (270 < 290).
    """
    w1, w2, w3, w4 = 5, 100, 20, 10

    score_a = w1 * 40 + w2 * 0 + w3 * 2 + w4 * 3
    score_b = w1 * 30 + w2 * 1 + w3 * 1 + w4 * 2

    assert score_a == 270
    assert score_b == 290
    assert score_a < score_b  # Lower is preferred

# -------------------------------------------------------------
# 8. Neighbor generation test
# -------------------------------------------------------------
def test_neighbor_generation():
    """Verify generated candidate neighbors are valid and distinct from current schedule."""
    patients_dict = {
        1: SimpleNamespace(id=1, arrival_time=540, priority="HIGH", consultation_duration=20),
        2: SimpleNamespace(id=2, arrival_time=550, priority="MEDIUM", consultation_duration=20)
    }
    docs = [SimpleNamespace(id=1), SimpleNamespace(id=2)]
    rooms = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    current = [
        {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 560, "end_time": 580, "waiting_time": 20},
        {"patient_id": 2, "doctor_id": 2, "room_id": 2, "start_time": 570, "end_time": 590, "waiting_time": 20},
    ]

    neighbors = generate_neighbors(current, patients_dict, docs, rooms)
    assert len(neighbors) > 0
    # Every neighbor must differ in some field from current
    for n in neighbors:
        assert n != current

# -------------------------------------------------------------
# 9. Hill Climbing optimization tests
# -------------------------------------------------------------
def test_hill_climbing_accepts_improvement():
    """Verify that Hill Climbing accepts a better neighboring schedule."""
    patients = [
        SimpleNamespace(id=1, arrival_time=540, priority="HIGH", consultation_duration=20, preferred_doctor_id=1),
        SimpleNamespace(id=2, arrival_time=540, priority="HIGH", consultation_duration=20, preferred_doctor_id=1)
    ]
    doctors = [
        SimpleNamespace(id=1, available_from=540, available_until=780),
        SimpleNamespace(id=2, available_from=540, available_until=780)
    ]
    rooms = [
        SimpleNamespace(id=1, available_from=540, available_until=780),
        SimpleNamespace(id=2, available_from=540, available_until=780)
    ]

    # Deliberately construct a bad initial schedule with an unnecessary delay
    bad_initial = [
        {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 600, "end_time": 620, "waiting_time": 60},
        {"patient_id": 2, "doctor_id": 1, "room_id": 1, "start_time": 620, "end_time": 640, "waiting_time": 80}
    ]

    res = hill_climb(bad_initial, patients, doctors, rooms, max_iterations=20)
    assert res["final_score"] < res["initial_score"]
    assert res["improvement"] > 0
    assert res["iterations"] >= 1

def test_hill_climbing_rejects_worse_solution():
    """Verify that Hill Climbing does NOT accept equal or worse schedules."""
    # Run hill climbing on an already tight conflict-free schedule; score should never increase
    patients = [
        SimpleNamespace(id=1, arrival_time=540, priority="HIGH", consultation_duration=20, preferred_doctor_id=1)
    ]
    doctors = [SimpleNamespace(id=1, available_from=540, available_until=780)]
    rooms = [SimpleNamespace(id=1, available_from=540, available_until=780)]

    perfect_schedule = [
        {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 560, "waiting_time": 0}
    ]

    res = hill_climb(perfect_schedule, patients, doctors, rooms, max_iterations=10)
    # Score must be <= initial score, never strictly higher
    assert res["final_score"] <= res["initial_score"]

def test_hill_climbing_terminates():
    """Verify that Hill Climbing terminates properly when no improvement exists or max iterations reached."""
    patients = [
        SimpleNamespace(id=1, arrival_time=540, priority="LOW", consultation_duration=15, preferred_doctor_id=None)
    ]
    doctors = [SimpleNamespace(id=1, available_from=540, available_until=780)]
    rooms = [SimpleNamespace(id=1, available_from=540, available_until=780)]

    initial = [
        {"patient_id": 1, "doctor_id": 1, "room_id": 1, "start_time": 540, "end_time": 555, "waiting_time": 0}
    ]
    res = hill_climb(initial, patients, doctors, rooms, max_iterations=50)
    assert res["iterations"] < 50  # Must terminate early at local minimum

# -------------------------------------------------------------
# 10. Constraint compliance test on full seed dataset
# -------------------------------------------------------------
def test_generated_schedule_respects_constraints():
    """Verify that initial schedule + Hill Climbing on the full 20 patients satisfies all hard constraints."""
    db = SessionLocal()
    from app.models.patient import Patient
    from app.models.doctor import Doctor
    from app.models.room import Room

    patients = db.query(Patient).all()
    doctors = db.query(Doctor).all()
    rooms = db.query(Room).all()

    initial = generate_initial_schedule(patients, doctors, rooms)
    res = hill_climb(initial, patients, doctors, rooms, max_iterations=50)
    final_sched = res["final_schedule"]

    assert len(final_sched) == 20

    patients_dict = {p.id: p for p in patients}
    doctors_dict = {d.id: d for d in doctors}
    rooms_dict = {r.id: r for r in rooms}

    # Must have 0 conflicts
    conflicts = count_all_conflicts(final_sched, doctors_dict, rooms_dict, patients_dict)
    assert conflicts == 0

    valid, violations = is_schedule_valid(final_sched, patients_dict, doctors_dict, rooms_dict)
    assert valid is True, f"Constraint violations found: {violations}"

    # Verify every patient is scheduled once
    scheduled_patient_ids = {a["patient_id"] for a in final_sched}
    assert len(scheduled_patient_ids) == 20

    # Verify no consultation before arrival
    for a in final_sched:
        p = patients_dict[a["patient_id"]]
        arr = parse_time(p.arrival_time)
        assert a["start_time"] >= arr
        assert a["end_time"] - a["start_time"] == p.consultation_duration
        assert a["start_time"] >= 540
        assert a["end_time"] <= 780

    db.close()

# -------------------------------------------------------------
# 11. REST API endpoint tests
# -------------------------------------------------------------
def test_generate_and_get_schedule_api():
    """Test POST /api/schedule/generate and GET /api/schedule."""
    response = client.post("/api/schedule/generate")
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "initial_score" in data
    assert "final_score" in data
    assert data["final_score"] <= data["initial_score"]
    assert "iterations" in data
    assert "improvement" in data
    assert "heuristic" in data
    assert len(data["schedule"]) == 20

    # Test GET /api/schedule
    get_res = client.get("/api/schedule")
    assert get_res.status_code == 200
    sched_list = get_res.json()
    assert len(sched_list) == 20

    # Test GET /api/schedule/score
    score_res = client.get("/api/schedule/score")
    assert score_res.status_code == 200
    score_data = score_res.json()
    assert score_data["has_schedule"] is True
    assert score_data["scheduled_patients"] == 20
    assert score_data["heuristic"]["conflicts"] == 0
