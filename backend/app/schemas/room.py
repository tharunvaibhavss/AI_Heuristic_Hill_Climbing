import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

TIME_REGEX = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")

class RoomBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Consultation room name")
    available_from: str = Field("09:00", description="Start of room availability (HH:MM)")
    available_until: str = Field("13:00", description="End of room availability (HH:MM)")

    @field_validator("available_from", "available_until")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not TIME_REGEX.match(v):
            raise ValueError("Time must be in 24-hour HH:MM format (e.g., '09:00')")
        return v

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    available_from: Optional[str] = None
    available_until: Optional[str] = None

    @field_validator("available_from", "available_until")
    @classmethod
    def validate_time(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not TIME_REGEX.match(v):
            raise ValueError("Time must be in 24-hour HH:MM format (e.g., '09:00')")
        return v

class RoomResponse(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
