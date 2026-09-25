from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.schedule import Schedule
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("", response_model=List[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    """Fetch all registered doctors."""
    return db.query(Doctor).order_by(Doctor.id).all()

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Fetch a single doctor by ID."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with ID {doctor_id} not found")
    return doctor

@router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor_in: DoctorCreate, db: Session = Depends(get_db)):
    """Create a new doctor."""
    doctor = Doctor(
        name=doctor_in.name,
        available_from=doctor_in.available_from,
        available_until=doctor_in.available_until
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor_in: DoctorUpdate, db: Session = Depends(get_db)):
    """Update doctor details."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with ID {doctor_id} not found")

    update_data = doctor_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    return doctor

@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Delete a doctor and unassign preferred doctor references."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with ID {doctor_id} not found")

    # Clear preferred_doctor_id on any patients referencing this doctor
    db.query(Patient).filter(Patient.preferred_doctor_id == doctor_id).update({Patient.preferred_doctor_id: None})
    # Remove any schedule entries for this doctor
    db.query(Schedule).filter(Schedule.doctor_id == doctor_id).delete()
    db.delete(doctor)
    db.commit()
    return None

