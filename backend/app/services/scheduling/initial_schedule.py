"""
Deterministic Initial Schedule Generator for Hospital Consultations.

Strategy:
1. Priority-first ordering: HIGH -> MEDIUM -> LOW
2. Within same priority: Earliest arrival time first
3. Doctor preference: Try preferred doctor first, then fallback to other doctors
4. Earliest feasible conflict-free slot: Earliest time interval [start, start + duration)
   where both selected doctor and room are available.
"""

from typing import List, Dict, Any
from app.services.scheduling.time_utils import parse_time, overlaps

def generate_initial_schedule(
    patients: List[Any],
    doctors: List[Any],
    rooms: List[Any],
    work_day_start: int = 540,  # 09:00 AM in minutes
    work_day_end: int = 780     # 01:00 PM in minutes
) -> List[Dict[str, Any]]:
    """
    Generates a deterministic, conflict-free initial schedule.
    Returns a list of appointment dictionaries with internal minute representation.
    """
    # Build doctor and room lookups
    doctors_dict = {d.id: d for d in doctors}
    rooms_dict = {r.id: r for r in rooms}

    # Priority ordering map
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

    def patient_sort_key(p):
        p_val = p.priority.value if hasattr(p.priority, "value") else str(p.priority)
        arrival = p.arrival_time if isinstance(p.arrival_time, int) else parse_time(p.arrival_time)
        return (priority_order.get(p_val, 1), arrival, p.id)

    sorted_patients = sorted(patients, key=patient_sort_key)

    schedule: List[Dict[str, Any]] = []

    for patient in sorted_patients:
        arrival = patient.arrival_time if isinstance(patient.arrival_time, int) else parse_time(patient.arrival_time)
        duration = patient.consultation_duration
        pref_doc_id = patient.preferred_doctor_id

        # Order doctor candidates: preferred doctor first (if valid), followed by others
        doctor_candidates = []
        if pref_doc_id and pref_doc_id in doctors_dict:
            doctor_candidates.append(doctors_dict[pref_doc_id])
        for doc in doctors:
            if doc not in doctor_candidates:
                doctor_candidates.append(doc)

        best_slot = None
        earliest_start_found = float("inf")

        # Search for earliest feasible slot
        # Discrete step of 5 minutes between max(arrival, work_day_start) and work_day_end - duration
        earliest_possible = max(arrival, work_day_start)
        latest_possible = work_day_end - duration

        # We evaluate slot options
        for doc in doctor_candidates:
            doc_from = doc.available_from if isinstance(doc.available_from, int) else parse_time(doc.available_from)
            doc_until = doc.available_until if isinstance(doc.available_until, int) else parse_time(doc.available_until)

            for room in rooms:
                room_from = room.available_from if isinstance(room.available_from, int) else parse_time(room.available_from)
                room_until = room.available_until if isinstance(room.available_until, int) else parse_time(room.available_until)

                search_start = max(earliest_possible, doc_from, room_from)
                search_end = min(latest_possible, doc_until - duration, room_until - duration)

                if search_start > search_end:
                    continue

                for t in range(search_start, search_end + 1, 5):
                    t_end = t + duration

                    # Check doctor conflict with already scheduled
                    doc_conflict = any(
                        appt["doctor_id"] == doc.id and overlaps(t, t_end, appt["start_time"], appt["end_time"])
                        for appt in schedule
                    )
                    if doc_conflict:
                        continue

                    # Check room conflict with already scheduled
                    room_conflict = any(
                        appt["room_id"] == room.id and overlaps(t, t_end, appt["start_time"], appt["end_time"])
                        for appt in schedule
                    )
                    if room_conflict:
                        continue

                    # Feasible slot found!
                    # Give preference to preferred doctor at same time
                    is_pref = 1 if (pref_doc_id and doc.id == pref_doc_id) else 0

                    if t < earliest_start_found:
                        earliest_start_found = t
                        best_slot = {
                            "doctor_id": doc.id,
                            "room_id": room.id,
                            "start_time": t,
                            "end_time": t_end,
                            "is_pref": is_pref
                        }
                    elif t == earliest_start_found and is_pref and best_slot and not best_slot.get("is_pref"):
                        best_slot = {
                            "doctor_id": doc.id,
                            "room_id": room.id,
                            "start_time": t,
                            "end_time": t_end,
                            "is_pref": is_pref
                        }
                    # Earliest found for this doc/room combination, proceed to next
                    break

            # If we found a conflict-free slot with preferred doctor at arrival time, accept immediately
            if best_slot and best_slot["start_time"] == earliest_possible and best_slot.get("is_pref"):
                break

        # If a conflict-free slot was found:
        if best_slot:
            waiting_time = max(0, best_slot["start_time"] - arrival)
            schedule.append({
                "patient_id": patient.id,
                "doctor_id": best_slot["doctor_id"],
                "room_id": best_slot["room_id"],
                "start_time": best_slot["start_time"],
                "end_time": best_slot["end_time"],
                "waiting_time": waiting_time
            })
        else:
            # Fallback (should rarely occur with 4 docs and 3 rooms):
            # Assign first available doctor & room at earliest_possible
            doc = doctor_candidates[0] if doctor_candidates else doctors[0]
            room = rooms[0]
            start_t = earliest_possible
            end_t = min(work_day_end, start_t + duration)
            waiting_time = max(0, start_t - arrival)
            schedule.append({
                "patient_id": patient.id,
                "doctor_id": doc.id,
                "room_id": room.id,
                "start_time": start_t,
                "end_time": end_t,
                "waiting_time": waiting_time
            })

    return schedule
