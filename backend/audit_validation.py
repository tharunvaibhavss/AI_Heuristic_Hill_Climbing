"""
Complete End-to-End Validation, Mathematical Audit, and Performance Benchmark.
Tests and audits all 20 requirements specified in Phase 4.
"""

import time
import json
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.room import Room
from app.models.schedule import Schedule
from app.services.seed import seed_database
from app.services.scheduling import parse_time, format_time, overlaps

client = TestClient(app)

def run_audit():
    print("=" * 70)
    print("PHASE 4: HOSPITAL SCHEDULING ENGINE END-TO-END AUDIT")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Database Reset & Seed Audit
    # ---------------------------------------------------------
    print("\n[Step 1] Database Reset & Seed Verification...")
    reset_res = client.post("/api/seed/reset")
    assert reset_res.status_code == 200, f"Reset failed: {reset_res.text}"
    reset_data = reset_res.json()
    print(f"  Reset response: {reset_data}")

    db = SessionLocal()
    patients = db.query(Patient).all()
    doctors = db.query(Doctor).all()
    rooms = db.query(Room).all()

    assert len(patients) == 20, f"Expected 20 patients, found {len(patients)}"
    assert len(doctors) == 4, f"Expected 4 doctors, found {len(doctors)}"
    assert len(rooms) == 3, f"Expected 3 rooms, found {len(rooms)}"

    for p in patients:
        arr_min = parse_time(p.arrival_time)
        assert 540 <= arr_min <= 780, f"Patient {p.name} invalid arrival: {p.arrival_time}"
        assert p.priority.value in ["HIGH", "MEDIUM", "LOW"]
        assert 10 <= p.consultation_duration <= 30
    for d in doctors:
        assert parse_time(d.available_from) == 540 and parse_time(d.available_until) == 780
    for r in rooms:
        assert parse_time(r.available_from) == 540 and parse_time(r.available_until) == 780
    print("  Seed verification: 20 patients, 4 doctors, 3 rooms verified valid.")

    # ---------------------------------------------------------
    # 2. Performance Measurement & Schedule Generation
    # ---------------------------------------------------------
    print("\n[Step 2] Schedule Generation & Timing Audit...")
    t0 = time.perf_counter()
    gen_res = client.post("/api/schedule/generate")
    t_total = (time.perf_counter() - t0) * 1000.0

    assert gen_res.status_code == 200, f"Generate failed: {gen_res.text}"
    gen_data = gen_res.json()

    initial_score = gen_data["initial_score"]
    final_score = gen_data["final_score"]
    iterations = gen_data["iterations"]
    improvement = gen_data["improvement"]
    heuristic = gen_data["heuristic"]
    sched_list = gen_data["schedule"]

    print(f"  Total API Response Time: {t_total:.2f} ms")
    print(f"  Scheduled Patients: {len(sched_list)} of 20")
    print(f"  Initial Score: {initial_score}")
    print(f"  Final Score:   {final_score}")
    print(f"  Improvement:   {improvement} ({(improvement/initial_score*100) if initial_score else 0:.1f}%)")
    print(f"  Iterations:    {iterations}")

    assert len(sched_list) == 20, f"Expected all 20 patients scheduled, got {len(sched_list)}"
    assert final_score <= initial_score, "Final score must be <= initial score"

    # ---------------------------------------------------------
    # 3. Schedule Constraints & Overlap Audit
    # ---------------------------------------------------------
    print("\n[Step 3] Hard Constraints & Overlap Audit...")
    scheduled_patient_ids = set()
    patients_dict = {p.id: p for p in patients}
    doctors_dict = {d.id: d for d in doctors}
    rooms_dict = {r.id: r for r in rooms}

    for item in sched_list:
        p_id = item["patient_id"]
        assert p_id not in scheduled_patient_ids, f"Duplicate patient {p_id}"
        scheduled_patient_ids.add(p_id)

        p = patients_dict[p_id]
        s_min = parse_time(item["start_time"])
        e_min = parse_time(item["end_time"])
        arr_min = parse_time(p.arrival_time)

        assert s_min >= arr_min, f"Start {s_min} < arrival {arr_min} for patient {p.name}"
        assert e_min > s_min, f"End {e_min} <= start {s_min}"
        assert (e_min - s_min) == p.consultation_duration, f"Duration mismatch for patient {p.name}"
        assert s_min >= 540, "Start before 09:00"
        assert e_min <= 780, "End after 13:00"

    # Pairwise doctor & room overlap audit
    n = len(sched_list)
    doc_conflicts = 0
    room_conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            a1 = sched_list[i]
            a2 = sched_list[j]
            s1, e1 = parse_time(a1["start_time"]), parse_time(a1["end_time"])
            s2, e2 = parse_time(a2["start_time"]), parse_time(a2["end_time"])

            if a1["doctor_id"] == a2["doctor_id"]:
                if overlaps(s1, e1, s2, e2):
                    doc_conflicts += 1
                    print(f"  Conflict: Doctor {a1['doctor_id']} overlapping between P#{a1['patient_id']} and P#{a2['patient_id']}")

            if a1["room_id"] == a2["room_id"]:
                if overlaps(s1, e1, s2, e2):
                    room_conflicts += 1
                    print(f"  Conflict: Room {a1['room_id']} overlapping between P#{a1['patient_id']} and P#{a2['patient_id']}")

    assert doc_conflicts == 0, f"Found {doc_conflicts} doctor overlaps!"
    assert room_conflicts == 0, f"Found {room_conflicts} room overlaps!"
    print(f"  Exhaustive pairwise conflict check: 0 doctor conflicts, 0 room conflicts across all {n*(n-1)//2} pairs.")

    # ---------------------------------------------------------
    # 4. Waiting Time Audit
    # ---------------------------------------------------------
    print("\n[Step 4] Waiting Time Audit...")
    manual_total_wait = 0
    for item in sched_list:
        p = patients_dict[item["patient_id"]]
        arr_min = parse_time(p.arrival_time)
        s_min = parse_time(item["start_time"])
        manual_wait = s_min - arr_min
        stored_wait = item["waiting_time"]
        assert manual_wait == stored_wait, f"Wait time mismatch for P#{p.id}: {manual_wait} != {stored_wait}"
        manual_total_wait += manual_wait

    assert manual_total_wait == heuristic["waiting_time"], (
        f"Total waiting time mismatch: manual {manual_total_wait} != heuristic {heuristic['waiting_time']}"
    )
    avg_wait = manual_total_wait / 20.0
    print(f"  Manual total wait: {manual_total_wait} min. Heuristic reported: {heuristic['waiting_time']} min. (MATCH)")
    print(f"  Average wait time: {avg_wait:.1f} min per patient.")

    # ---------------------------------------------------------
    # 5. Heuristic Score Verification
    # ---------------------------------------------------------
    print("\n[Step 5] Independent Heuristic Formula Calculation...")
    wt = heuristic["waiting_time"]
    c = heuristic["conflicts"]
    p_pen = heuristic["priority_penalty"]
    u = heuristic["under_utilization"]

    manual_score = round(5 * wt + 100 * c + 20 * p_pen + 10 * u, 2)
    api_score = heuristic["total_score"]
    assert manual_score == api_score, f"Score mismatch: {manual_score} != {api_score}"

    # Also verify GET /api/schedule/score
    score_res = client.get("/api/schedule/score")
    assert score_res.status_code == 200
    score_data = score_res.json()
    assert score_data["heuristic"]["total_score"] == api_score
    print(f"  Formula: 5({wt}) + 100({c}) + 20({p_pen}) + 10({u}) = {manual_score}")
    print(f"  API GET /api/schedule/score matches exactly: {score_data['heuristic']['total_score']}.")

    # ---------------------------------------------------------
    # 6. Resource Utilization Audit
    # ---------------------------------------------------------
    print("\n[Step 6] Resource Utilization Audit...")
    doc_minutes = {d.id: 0 for d in doctors}
    room_minutes = {r.id: 0 for r in rooms}
    total_consult_minutes = 0

    for item in sched_list:
        dur = parse_time(item["end_time"]) - parse_time(item["start_time"])
        doc_minutes[item["doctor_id"]] += dur
        room_minutes[item["room_id"]] += dur
        total_consult_minutes += dur

    print(f"  Total Consultation Minutes: {total_consult_minutes} min")
    for d in doctors:
        used = doc_minutes[d.id]
        util_pct = (used / 240.0) * 100.0
        print(f"    Doctor #{d.id} ({d.name}): {used}m / 240m ({util_pct:.1f}%)")

    for r in rooms:
        used = room_minutes[r.id]
        util_pct = (used / 240.0) * 100.0
        print(f"    Room #{r.id} ({r.name}): {used}m / 240m ({util_pct:.1f}%)")

    # ---------------------------------------------------------
    # 7. Priority Analysis
    # ---------------------------------------------------------
    print("\n[Step 7] Priority Triage Waiting Times...")
    for prio in ["HIGH", "MEDIUM", "LOW"]:
        prio_waits = [
            item["waiting_time"] for item in sched_list
            if patients_dict[item["patient_id"]].priority.value == prio
        ]
        avg_p = sum(prio_waits) / len(prio_waits) if prio_waits else 0
        max_p = max(prio_waits) if prio_waits else 0
        min_p = min(prio_waits) if prio_waits else 0
        print(f"    Priority {prio:<6}: Count={len(prio_waits)}, Avg Wait={avg_p:.1f}m, Min={min_p}m, Max={max_p}m")

    # ---------------------------------------------------------
    # 8. Preferred Doctor Compliance Audit
    # ---------------------------------------------------------
    print("\n[Step 8] Preferred Doctor Compliance...")
    pref_match = 0
    pref_total = 0
    for item in sched_list:
        p = patients_dict[item["patient_id"]]
        if p.preferred_doctor_id is not None:
            pref_total += 1
            if item["doctor_id"] == p.preferred_doctor_id:
                pref_match += 1
    print(f"    Preferred Doctor Matched: {pref_match} of {pref_total} patients who had a preference ({(pref_match/pref_total*100) if pref_total else 0:.1f}%).")

    # ---------------------------------------------------------
    # 9. Database Idempotency / Double Generation Test
    # ---------------------------------------------------------
    print("\n[Step 9] Database Idempotency & Unique Constraint Audit...")
    client.post("/api/schedule/generate")
    db2 = SessionLocal()
    count_after_regen = db2.query(Schedule).count()
    assert count_after_regen == 20, f"Expected 20 records after second generate, found {count_after_regen}!"
    db2.close()
    print("  Regenerated schedule successfully replaced previous records with exactly 20 unique rows.")

    # ---------------------------------------------------------
    # 10. Invalid Input Validation Tests
    # ---------------------------------------------------------
    print("\n[Step 10] Invalid Input Rejection Audit...")
    # Consultation duration < 10
    res1 = client.post("/api/patients", json={
        "name": "Invalid Too Short", "arrival_time": "09:00", "priority": "HIGH", "consultation_duration": 5
    })
    assert res1.status_code == 422, f"Expected 422, got {res1.status_code}"

    # Consultation duration > 30
    res2 = client.post("/api/patients", json={
        "name": "Invalid Too Long", "arrival_time": "09:00", "priority": "HIGH", "consultation_duration": 45
    })
    assert res2.status_code == 422, f"Expected 422, got {res2.status_code}"

    # Invalid arrival time
    res3 = client.post("/api/patients", json={
        "name": "Invalid Time", "arrival_time": "25:99", "priority": "MEDIUM", "consultation_duration": 20
    })
    assert res3.status_code == 422, f"Expected 422, got {res3.status_code}"

    # Missing patient name
    res4 = client.post("/api/patients", json={
        "arrival_time": "09:15", "priority": "LOW", "consultation_duration": 15
    })
    assert res4.status_code == 422, f"Expected 422, got {res4.status_code}"
    print("  Input validation correctly rejected all invalid payloads with HTTP 422.")

    # ---------------------------------------------------------
    # 11. Edge Case Tests
    # ---------------------------------------------------------
    print("\n[Step 11] Edge Case Scenario Testing...")
    # Edge arrival at 12:30 (last 30 min of hospital day)
    edge_p = client.post("/api/patients", json={
        "name": "Late Arrival Patient", "arrival_time": "12:30", "priority": "HIGH", "consultation_duration": 25
    })
    assert edge_p.status_code == 201
    edge_p_data = edge_p.json()

    # Regenerate with 21 patients
    gen_edge = client.post("/api/schedule/generate")
    assert gen_edge.status_code == 200
    edge_sched = gen_edge.json()["schedule"]
    late_item = next(item for item in edge_sched if item["patient_id"] == edge_p_data["id"])
    assert late_item["start_time"] >= "12:30"
    assert late_item["end_time"] <= "13:00"
    print(f"  Late patient (12:30) scheduled successfully: {late_item['start_time']} - {late_item['end_time']}.")

    # Clean up test patient and restore seed
    client.delete(f"/api/patients/{edge_p_data['id']}")
    client.post("/api/seed/reset")
    client.post("/api/schedule/generate")
    print("  Cleaned up edge test patient and restored clean benchmark state.")

    db.close()
    print("\n" + "=" * 70)
    print("ALL AUDIT STEPS PASSED SUCCESSFULLY (100% CORRECTNESS VERIFIED)")
    print("=" * 70)

if __name__ == "__main__":
    run_audit()
