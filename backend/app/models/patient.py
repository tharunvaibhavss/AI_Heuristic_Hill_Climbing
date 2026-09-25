import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class PriorityEnum(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    arrival_time = Column(String(5), nullable=False)  # HH:MM format, e.g. "09:15"
    priority = Column(SQLEnum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    consultation_duration = Column(Integer, nullable=False)  # In minutes: 10 to 30
    preferred_doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    preferred_doctor = relationship("Doctor", back_populates="preferred_patients")
    schedule_entry = relationship("Schedule", back_populates="patient", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, name='{self.name}', priority='{self.priority.value}', arrival='{self.arrival_time}')>"
