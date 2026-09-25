from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.schedule import Schedule
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    """Fetch all patients with preferred doctor relationship."""
    return db.query(Patient).options(joinedload(Patient.preferred_doctor)).order_by(Patient.id).all()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Fetch a single patient by ID."""
    patient = db.query(Patient).options(joinedload(Patient.preferred_doctor)).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID {patient_id} not found")
    return patient

@router.post("", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient."""
    if patient_in.preferred_doctor_id is not None:
        doc = db.query(Doctor).filter(Doctor.id == patient_in.preferred_doctor_id).first()
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Preferred doctor with ID {patient_in.preferred_doctor_id} does not exist"
            )

    patient = Patient(
        name=patient_in.name,
        arrival_time=patient_in.arrival_time,
        priority=patient_in.priority,
        consultation_duration=patient_in.consultation_duration,
        preferred_doctor_id=patient_in.preferred_doctor_id
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient_in: PatientUpdate, db: Session = Depends(get_db)):
    """Update patient details."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID {patient_id} not found")

    if patient_in.preferred_doctor_id is not None:
        doc = db.query(Doctor).filter(Doctor.id == patient_in.preferred_doctor_id).first()
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Preferred doctor with ID {patient_in.preferred_doctor_id} does not exist"
            )

    update_data = patient_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient and any associated scheduled appointments."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID {patient_id} not found")

    # Clean up any schedule entry for this patient
    db.query(Schedule).filter(Schedule.patient_id == patient_id).delete()
    db.delete(patient)
    db.commit()
    return None
