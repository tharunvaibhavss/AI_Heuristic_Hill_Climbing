"""Hard constraint validation and conflict detection for patient schedules."""

from typing import List, Dict, Any, Tuple
from app.services.scheduling.time_utils import overlaps, parse_time

def is_doctor_available(
    doctor_id: int,
    start_time: int,
    end_time: int,
    doctors_dict: Dict[int, Any]
) -> bool:
    """Check if the consultation interval is within doctor operating hours."""
    doc = doctors_dict.get(doctor_id)
    if not doc:
        return False
    doc_from = doc.available_from if isinstance(doc.available_from, int) else parse_time(doc.available_from)
    doc_until = doc.available_until if isinstance(doc.available_until, int) else parse_time(doc.available_until)
    return start_time >= doc_from and end_time <= doc_until

def is_room_available(
    room_id: int,
    start_time: int,
    end_time: int,
    rooms_dict: Dict[int, Any]
) -> bool:
    """Check if the consultation interval is within room operating hours."""
    room = rooms_dict.get(room_id)
    if not room:
        return False
    room_from = room.available_from if isinstance(room.available_from, int) else parse_time(room.available_from)
    room_until = room.available_until if isinstance(room.available_until, int) else parse_time(room.available_until)
    return start_time >= room_from and end_time <= room_until

def has_doctor_conflict(appt1: Dict[str, Any], appt2: Dict[str, Any]) -> bool:
    """Check if two appointments share the same doctor and overlap in time."""
    if appt1["doctor_id"] != appt2["doctor_id"]:
        return False
    return overlaps(
        appt1["start_time"], appt1["end_time"],
        appt2["start_time"], appt2["end_time"]
    )

def has_room_conflict(appt1: Dict[str, Any], appt2: Dict[str, Any]) -> bool:
    """Check if two appointments share the same room and overlap in time."""
    if appt1["room_id"] != appt2["room_id"]:
        return False
    return overlaps(
        appt1["start_time"], appt1["end_time"],
        appt2["start_time"], appt2["end_time"]
    )

def is_patient_valid(appt: Dict[str, Any], patient: Any) -> Tuple[bool, str]:
    """Validate that appointment meets patient arrival and duration constraints."""
    arrival = patient.arrival_time if isinstance(patient.arrival_time, int) else parse_time(patient.arrival_time)
    start = appt["start_time"]
    end = appt["end_time"]
    duration = end - start

    if start < arrival:
        return False, f"Start time {start} is before arrival time {arrival}"
    if duration != patient.consultation_duration:
        return False, f"Duration {duration} does not match expected {patient.consultation_duration}"
    if not (10 <= duration <= 30):
        return False, f"Duration {duration} out of allowed 10-30 min range"
    return True, ""

def count_all_conflicts(
    schedule: List[Dict[str, Any]],
    doctors_dict: Dict[int, Any] = None,
    rooms_dict: Dict[int, Any] = None,
    patients_dict: Dict[int, Any] = None
) -> int:
    """
    Count the total number of hard conflicts in a schedule.
    Conflicts include:
    1. Pairwise doctor overlaps (same doctor, overlapping time)
    2. Pairwise room overlaps (same room, overlapping time)
    3. Pairwise patient duplicates (same patient scheduled multiple times)
    4. Doctor shift violations (start < available_from or end > available_until)
    5. Room availability violations (start < available_from or end > available_until)
    6. Patient arrival violations (start < arrival_time)
    """
    conflicts = 0
    n = len(schedule)

    # 1. Pairwise checks (O(N^2) for N=20 is ~190 comparisons, microsecond fast)
    for i in range(n):
        for j in range(i + 1, n):
            a1 = schedule[i]
            a2 = schedule[j]

            # Doctor overlap
            if has_doctor_conflict(a1, a2):
                conflicts += 1

            # Room overlap
            if has_room_conflict(a1, a2):
                conflicts += 1

            # Duplicate patient
            if a1["patient_id"] == a2["patient_id"]:
                conflicts += 1

    # 2. Individual appointment boundary and arrival checks
    for appt in schedule:
        start = appt["start_time"]
        end = appt["end_time"]

        # Doctor availability
        if doctors_dict:
            if not is_doctor_available(appt["doctor_id"], start, end, doctors_dict):
                conflicts += 1

        # Room availability
        if rooms_dict:
            if not is_room_available(appt["room_id"], start, end, rooms_dict):
                conflicts += 1

        # Patient arrival
        if patients_dict:
            p = patients_dict.get(appt["patient_id"])
            if p:
                arrival = p.arrival_time if isinstance(p.arrival_time, int) else parse_time(p.arrival_time)
                if start < arrival:
                    conflicts += 1

    return conflicts

def is_schedule_valid(
    schedule: List[Dict[str, Any]],
    patients_dict: Dict[int, Any],
    doctors_dict: Dict[int, Any],
    rooms_dict: Dict[int, Any]
) -> Tuple[bool, List[str]]:
    """Returns whether a schedule has zero conflicts, and lists all violations."""
    violations = []
    n = len(schedule)

    # Check pairwise conflicts
    for i in range(n):
        for j in range(i + 1, n):
            a1 = schedule[i]
            a2 = schedule[j]

            if has_doctor_conflict(a1, a2):
                violations.append(
                    f"Doctor overlap: Doctor {a1['doctor_id']} has overlapping patients "
                    f"{a1['patient_id']} ({a1['start_time']}-{a1['end_time']}) and "
                    f"{a2['patient_id']} ({a2['start_time']}-{a2['end_time']})"
                )

            if has_room_conflict(a1, a2):
                violations.append(
                    f"Room overlap: Room {a1['room_id']} has overlapping patients "
                    f"{a1['patient_id']} ({a1['start_time']}-{a1['end_time']}) and "
                    f"{a2['patient_id']} ({a2['start_time']}-{a2['end_time']})"
                )

            if a1["patient_id"] == a2["patient_id"]:
                violations.append(f"Duplicate patient {a1['patient_id']} scheduled multiple times")

    # Check individual bounds
    for appt in schedule:
        p = patients_dict.get(appt["patient_id"])
        if p:
            valid, err = is_patient_valid(appt, p)
            if not valid:
                violations.append(f"Patient {p.id}: {err}")

        if not is_doctor_available(appt["doctor_id"], appt["start_time"], appt["end_time"], doctors_dict):
            violations.append(f"Doctor {appt['doctor_id']} outside availability for appt {appt}")

        if not is_room_available(appt["room_id"], appt["start_time"], appt["end_time"], rooms_dict):
            violations.append(f"Room {appt['room_id']} outside availability for appt {appt}")

    return len(violations) == 0, violations
