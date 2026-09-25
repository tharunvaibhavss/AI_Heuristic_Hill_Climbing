from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.patient import PatientResponse
from app.schemas.doctor import DoctorResponse
from app.schemas.room import RoomResponse

class ScheduleBase(BaseModel):
    patient_id: int
    doctor_id: int
    room_id: int
    start_time: str
    end_time: str
    waiting_time: int = 0

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None
    room: Optional[RoomResponse] = None

class HeuristicBreakdown(BaseModel):
    total_waiting_time: float
    conflicts: int
    priority_penalty: float
    under_utilization: float
    weighted_waiting_cost: float
    weighted_conflict_cost: float
    weighted_priority_cost: float
    weighted_utilization_cost: float
    total_heuristic_score: float

class ScheduleGenerationResponse(BaseModel):
    success: bool
    initial_score: float
    final_score: float
    iterations: int
    improvement: float
    accepted_moves: int = 0
    neighbor_evaluations: int = 0
    status_message: str = "Local minimum reached"
    heuristic: Dict[str, Any]
    schedule: List[ScheduleResponse]

