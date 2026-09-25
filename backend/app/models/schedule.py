from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, unique=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(String(5), nullable=False)  # HH:MM
    end_time = Column(String(5), nullable=False)    # HH:MM
    waiting_time = Column(Integer, nullable=False, default=0)  # Waiting time in minutes
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    patient = relationship("Patient", back_populates="schedule_entry")
    doctor = relationship("Doctor", back_populates="schedule_entries")
    room = relationship("Room", back_populates="schedule_entries")

    def __repr__(self):
        return f"<Schedule(patient_id={self.patient_id}, doctor_id={self.doctor_id}, room_id={self.room_id}, time='{self.start_time}-{self.end_time}')>"
