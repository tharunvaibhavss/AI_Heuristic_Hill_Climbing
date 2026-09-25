from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
import re
from app.models.patient import PriorityEnum
from app.schemas.doctor import DoctorResponse

TIME_REGEX = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")

class PatientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Patient full name")
    arrival_time: str = Field(..., description="Arrival time in HH:MM format (e.g., '09:15')")
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, description="Priority: HIGH, MEDIUM, LOW")
    consultation_duration: int = Field(..., ge=10, le=30, description="Expected consultation duration (10 to 30 mins)")
    preferred_doctor_id: Optional[int] = Field(None, description="Preferred doctor ID, if any")

    @field_validator("arrival_time")
    @classmethod
    def validate_arrival_time(cls, v: str) -> str:
        if not TIME_REGEX.match(v):
            raise ValueError("Arrival time must be in 24-hour HH:MM format (e.g., '09:15')")
        return v

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    arrival_time: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    consultation_duration: Optional[int] = Field(None, ge=10, le=30)
    preferred_doctor_id: Optional[int] = None

    @field_validator("arrival_time")
    @classmethod
    def validate_arrival_time(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not TIME_REGEX.match(v):
            raise ValueError("Arrival time must be in 24-hour HH:MM format (e.g., '09:15')")
        return v

class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    preferred_doctor: Optional[DoctorResponse] = None
