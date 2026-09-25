from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.seed import seed_database
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.room import Room

router = APIRouter(prefix="/seed", tags=["Seed Data"])

@router.post("/reset")
def reset_seed_data(db: Session = Depends(get_db)):
    """Reset and re-seed the database with 20 patients, 4 doctors, and 3 rooms."""
    seed_database(db, force_reset=True)
    return {
        "message": "Database reset and seeded successfully",
        "patients_count": db.query(Patient).count(),
        "doctors_count": db.query(Doctor).count(),
        "rooms_count": db.query(Room).count()
    }
