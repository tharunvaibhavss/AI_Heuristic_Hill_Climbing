from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.room import Room
from app.models.schedule import Schedule

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    patient_count = db.query(Patient).count() if db_status == "connected" else 0
    doctor_count = db.query(Doctor).count() if db_status == "connected" else 0
    room_count = db.query(Room).count() if db_status == "connected" else 0
    scheduled_count = db.query(Schedule).count() if db_status == "connected" else 0

    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": {
            "status": db_status,
            "patient_count": patient_count,
            "doctor_count": doctor_count,
            "room_count": room_count,
            "scheduled_count": scheduled_count
        },
        "version": "1.0.0"
    }
