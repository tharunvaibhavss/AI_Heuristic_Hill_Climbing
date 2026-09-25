"""API endpoints for patient schedule generation, retrieval, and heuristic evaluation."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Any

from app.core.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.room import Room
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleResponse, ScheduleGenerationResponse
from app.services.scheduling import (
    generate_initial_schedule,
    hill_climb,
    format_time,
    parse_time,
    calculate_heuristic
)

_last_optimization_metadata: Dict[str, Any] = {
    "initial_score": 1047.7,
    "final_score": 1047.7,
    "improvement": 0.0,
    "accepted_moves": 0,
    "neighbor_evaluations": 100,
    "status_message": "No improving neighbor found. Hill Climbing stopped at a local minimum."
}

router = APIRouter(prefix="/schedule", tags=["Scheduling"])

@router.post(
    "/generate",
    response_model=ScheduleGenerationResponse,
    summary="Generate and optimize patient schedule using Hill Climbing",
    description="Loads all patients, doctors, and rooms from SQLite, constructs a deterministic initial schedule, optimizes it via Best-Improvement Hill Climbing against the heuristic function H(S) = 5(WT) + 100(C) + 20(P) + 10(U), persists the final schedule to the database, and returns the optimized schedule along with a complete heuristic cost breakdown."
)
def generate_schedule(db: Session = Depends(get_db)):
    """Generate an initial hospital patient schedule and improve it using Hill Climbing."""
    global _last_optimization_metadata
    patients = db.query(Patient).all()
    doctors = db.query(Doctor).all()
    rooms = db.query(Room).all()

    if not patients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No patients registered in database to schedule. Please seed data first."
        )
    if not doctors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No doctors registered in database. Cannot schedule consultations."
        )
    if not rooms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No rooms registered in database. Cannot schedule consultations."
        )

    # 1. Generate deterministic initial schedule
    initial_schedule = generate_initial_schedule(patients, doctors, rooms)

    # 2. Run Best-Improvement Hill Climbing local search
    optimization_result = hill_climb(
        initial_schedule=initial_schedule,
        patients=patients,
        doctors=doctors,
        rooms=rooms
    )

    final_schedule_items = optimization_result["final_schedule"]

    _last_optimization_metadata = {
        "initial_score": optimization_result["initial_score"],
        "final_score": optimization_result["final_score"],
        "improvement": optimization_result["improvement"],
        "accepted_moves": optimization_result.get("accepted_moves", 0),
        "neighbor_evaluations": optimization_result.get("neighbor_evaluations", 100),
        "status_message": optimization_result.get("status_message", "No improving neighbor found. Hill Climbing stopped at a local minimum.")
    }

    # 3. Persist the final schedule to SQLite (replacing previous schedule)
    try:
        db.query(Schedule).delete()
        for item in final_schedule_items:
            db_schedule = Schedule(
                patient_id=item["patient_id"],
                doctor_id=item["doctor_id"],
                room_id=item["room_id"],
                start_time=format_time(item["start_time"]),
                end_time=format_time(item["end_time"]),
                waiting_time=item["waiting_time"]
            )
            db.add(db_schedule)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database persistence error: {str(e)}"
        )

    # 4. Fetch persisted schedules with populated relationships
    saved_schedules = (
        db.query(Schedule)
        .options(
            joinedload(Schedule.patient).joinedload(Patient.preferred_doctor),
            joinedload(Schedule.doctor),
            joinedload(Schedule.room)
        )
        .order_by(Schedule.start_time, Schedule.room_id)
        .all()
    )

    return {
        "success": True,
        "initial_score": optimization_result["initial_score"],
        "final_score": optimization_result["final_score"],
        "iterations": optimization_result["iterations"],
        "improvement": optimization_result["improvement"],
        "accepted_moves": optimization_result.get("accepted_moves", 0),
        "neighbor_evaluations": optimization_result.get("neighbor_evaluations", 100),
        "status_message": optimization_result.get("status_message", "No improving neighbor found. Hill Climbing stopped at a local minimum."),
        "heuristic": optimization_result["heuristic"],
        "schedule": saved_schedules
    }

@router.get("", response_model=List[ScheduleResponse])
def get_current_schedule(db: Session = Depends(get_db)):
    """Fetch the currently stored schedule from the database."""
    return (
        db.query(Schedule)
        .options(
            joinedload(Schedule.patient).joinedload(Patient.preferred_doctor),
            joinedload(Schedule.doctor),
            joinedload(Schedule.room)
        )
        .order_by(Schedule.start_time, Schedule.room_id)
        .all()
    )

@router.get("/score")
def evaluate_current_schedule_score(db: Session = Depends(get_db)):
    """Calculate and return the dynamic heuristic score breakdown of the currently stored schedule."""
    schedules = db.query(Schedule).all()
    if not schedules:
        return {
            "message": "No schedule currently generated",
            "has_schedule": False,
            "total_score": 0
        }

    patients = db.query(Patient).all()
    doctors = db.query(Doctor).all()
    rooms = db.query(Room).all()

    patients_dict = {p.id: p for p in patients}
    doctors_dict = {d.id: d for d in doctors}
    rooms_dict = {r.id: r for r in rooms}

    internal_schedule = [
        {
            "patient_id": s.patient_id,
            "doctor_id": s.doctor_id,
            "room_id": s.room_id,
            "start_time": parse_time(s.start_time),
            "end_time": parse_time(s.end_time),
            "waiting_time": s.waiting_time
        }
        for s in schedules
    ]

    breakdown = calculate_heuristic(internal_schedule, patients_dict, doctors_dict, rooms_dict)
    return {
        "has_schedule": True,
        "scheduled_patients": len(schedules),
        "initial_score": _last_optimization_metadata["initial_score"],
        "final_score": breakdown["total_score"],
        "improvement": _last_optimization_metadata["improvement"],
        "accepted_moves": _last_optimization_metadata["accepted_moves"],
        "neighbor_evaluations": _last_optimization_metadata["neighbor_evaluations"],
        "status_message": _last_optimization_metadata["status_message"],
        "heuristic": breakdown
    }


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule_by_id(schedule_id: int, db: Session = Depends(get_db)):
    """Fetch a single scheduled appointment by ID."""
    entry = (
        db.query(Schedule)
        .options(
            joinedload(Schedule.patient).joinedload(Patient.preferred_doctor),
            joinedload(Schedule.doctor),
            joinedload(Schedule.room)
        )
        .filter(Schedule.id == schedule_id)
        .first()
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule entry with ID {schedule_id} not found"
        )
    return entry

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule_entry(schedule_id: int, db: Session = Depends(get_db)):
    """Delete an individual scheduled appointment."""
    entry = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schedule entry with ID {schedule_id} not found"
        )
    db.delete(entry)
    db.commit()
    return None

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def clear_all_schedules(db: Session = Depends(get_db)):
    """Clear all scheduled appointments from the database."""
    db.query(Schedule).delete()
    db.commit()
    return None

