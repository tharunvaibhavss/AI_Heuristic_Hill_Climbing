"""Scheduling service package exposing core optimization and heuristic functions."""

from app.services.scheduling.time_utils import (
    parse_time,
    format_time,
    duration_between,
    overlaps
)
from app.services.scheduling.constraints import (
    is_doctor_available,
    is_room_available,
    has_doctor_conflict,
    has_room_conflict,
    is_patient_valid,
    count_all_conflicts,
    is_schedule_valid
)
from app.services.scheduling.heuristic import (
    calculate_total_waiting_time,
    calculate_conflicts,
    calculate_priority_penalty,
    calculate_under_utilization,
    calculate_heuristic
)
from app.services.scheduling.initial_schedule import generate_initial_schedule
from app.services.scheduling.neighbors import generate_neighbors
from app.services.scheduling.hill_climbing import hill_climb

__all__ = [
    "parse_time",
    "format_time",
    "duration_between",
    "overlaps",
    "is_doctor_available",
    "is_room_available",
    "has_doctor_conflict",
    "has_room_conflict",
    "is_patient_valid",
    "count_all_conflicts",
    "is_schedule_valid",
    "calculate_total_waiting_time",
    "calculate_conflicts",
    "calculate_priority_penalty",
    "calculate_under_utilization",
    "calculate_heuristic",
    "generate_initial_schedule",
    "generate_neighbors",
    "hill_climb",
]
