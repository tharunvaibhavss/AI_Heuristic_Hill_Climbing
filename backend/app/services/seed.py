from sqlalchemy.orm import Session
from app.models.patient import Patient, PriorityEnum
from app.models.doctor import Doctor
from app.models.room import Room
from app.models.schedule import Schedule

SEED_DOCTORS = [
    {"id": 1, "name": "Dr. Sarah Jenkins", "available_from": "09:00", "available_until": "13:00"},
    {"id": 2, "name": "Dr. Robert Chen", "available_from": "09:00", "available_until": "13:00"},
    {"id": 3, "name": "Dr. Emily Patel", "available_from": "09:00", "available_until": "13:00"},
    {"id": 4, "name": "Dr. Marcus Vance", "available_from": "09:00", "available_until": "13:00"},
]

SEED_ROOMS = [
    {"id": 1, "name": "Consultation Room A-101", "available_from": "09:00", "available_until": "13:00"},
    {"id": 2, "name": "Consultation Room B-102", "available_from": "09:00", "available_until": "13:00"},
    {"id": 3, "name": "Consultation Room C-103", "available_from": "09:00", "available_until": "13:00"},
]

SEED_PATIENTS = [
    # 1-5: High Priority (Emergencies / Acute cases)
    {"name": "Arthur Pendelton", "arrival_time": "09:00", "priority": PriorityEnum.HIGH, "consultation_duration": 25, "preferred_doctor_id": 1},
    {"name": "Beatrice Gomez", "arrival_time": "09:05", "priority": PriorityEnum.HIGH, "consultation_duration": 30, "preferred_doctor_id": 4},
    {"name": "Carlos Mendoza", "arrival_time": "09:20", "priority": PriorityEnum.HIGH, "consultation_duration": 20, "preferred_doctor_id": 2},
    {"name": "Diana Ross-Campbell", "arrival_time": "09:45", "priority": PriorityEnum.HIGH, "consultation_duration": 25, "preferred_doctor_id": 1},
    {"name": "Edward Hughes", "arrival_time": "10:15", "priority": PriorityEnum.HIGH, "consultation_duration": 20, "preferred_doctor_id": 4},

    # 6-14: Medium Priority (Urgent consultations & ongoing management)
    {"name": "Fiona Gallagher", "arrival_time": "09:10", "priority": PriorityEnum.MEDIUM, "consultation_duration": 15, "preferred_doctor_id": 3},
    {"name": "George Sterling", "arrival_time": "09:15", "priority": PriorityEnum.MEDIUM, "consultation_duration": 20, "preferred_doctor_id": 2},
    {"name": "Hannah Abbott", "arrival_time": "09:25", "priority": PriorityEnum.MEDIUM, "consultation_duration": 15, "preferred_doctor_id": None},
    {"name": "Isaac Newton-John", "arrival_time": "09:30", "priority": PriorityEnum.MEDIUM, "consultation_duration": 25, "preferred_doctor_id": 1},
    {"name": "Julia Roberts-Lee", "arrival_time": "09:50", "priority": PriorityEnum.MEDIUM, "consultation_duration": 20, "preferred_doctor_id": 3},
    {"name": "Kevin Peterson", "arrival_time": "10:00", "priority": PriorityEnum.MEDIUM, "consultation_duration": 15, "preferred_doctor_id": 2},
    {"name": "Laura Croft", "arrival_time": "10:05", "priority": PriorityEnum.MEDIUM, "consultation_duration": 30, "preferred_doctor_id": None},
    {"name": "Michael Chang", "arrival_time": "10:20", "priority": PriorityEnum.MEDIUM, "consultation_duration": 15, "preferred_doctor_id": 4},
    {"name": "Nadia Petrova", "arrival_time": "10:30", "priority": PriorityEnum.MEDIUM, "consultation_duration": 20, "preferred_doctor_id": 3},

    # 15-20: Low Priority (Routine follow-ups, minor refills & wellness)
    {"name": "Oliver Queen", "arrival_time": "09:40", "priority": PriorityEnum.LOW, "consultation_duration": 10, "preferred_doctor_id": None},
    {"name": "Patricia Walker", "arrival_time": "10:45", "priority": PriorityEnum.LOW, "consultation_duration": 15, "preferred_doctor_id": 1},
    {"name": "Quincy Adams", "arrival_time": "11:00", "priority": PriorityEnum.LOW, "consultation_duration": 10, "preferred_doctor_id": 2},
    {"name": "Rachel Zane", "arrival_time": "11:10", "priority": PriorityEnum.LOW, "consultation_duration": 20, "preferred_doctor_id": 3},
    {"name": "Samuel Jackson", "arrival_time": "11:15", "priority": PriorityEnum.LOW, "consultation_duration": 15, "preferred_doctor_id": None},
    {"name": "Tara Knowles", "arrival_time": "11:30", "priority": PriorityEnum.LOW, "consultation_duration": 10, "preferred_doctor_id": 4},
]

def seed_database(db: Session, force_reset: bool = False):
    """
    Seeds the SQLite database with 4 doctors, 3 rooms, and 20 patients.
    If force_reset is True, clears existing data first.
    """
    if force_reset:
        db.query(Schedule).delete()
        db.query(Patient).delete()
        db.query(Doctor).delete()
        db.query(Room).delete()
        db.commit()

    # Seed Doctors
    if db.query(Doctor).count() == 0:
        for doc_data in SEED_DOCTORS:
            doc = Doctor(
                id=doc_data["id"],
                name=doc_data["name"],
                available_from=doc_data["available_from"],
                available_until=doc_data["available_until"]
            )
            db.add(doc)
        db.commit()

    # Seed Rooms
    if db.query(Room).count() == 0:
        for room_data in SEED_ROOMS:
            room = Room(
                id=room_data["id"],
                name=room_data["name"],
                available_from=room_data["available_from"],
                available_until=room_data["available_until"]
            )
            db.add(room)
        db.commit()

    # Seed Patients
    if db.query(Patient).count() == 0:
        for p_data in SEED_PATIENTS:
            patient = Patient(
                name=p_data["name"],
                arrival_time=p_data["arrival_time"],
                priority=p_data["priority"],
                consultation_duration=p_data["consultation_duration"],
                preferred_doctor_id=p_data["preferred_doctor_id"]
            )
            db.add(patient)
        db.commit()
