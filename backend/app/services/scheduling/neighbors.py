"""
Neighbor generation service for Hill Climbing local search.

Neighborhood Operations:
1. Move Time: Shift a patient's consultation earlier or later by 5 or 10 minutes.
2. Change Doctor: Reassign a patient to another available doctor.
3. Change Room: Reassign a patient to another available consultation room.
4. Swap Patients: Swap assignments (doctor/room/time) between two patients.

A controlled, diverse set of candidate neighbors is generated on each iteration.
"""

import copy
from typing import List, Dict, Any
from app.services.scheduling.time_utils import parse_time

def generate_neighbors(
    current_schedule: List[Dict[str, Any]],
    patients_dict: Dict[int, Any],
    doctors: List[Any],
    rooms: List[Any],
    work_day_start: int = 540,
    work_day_end: int = 780,
    max_candidates_per_type: int = 25
) -> List[List[Dict[str, Any]]]:
    """
    Generates a controlled, diverse list of valid candidate neighboring schedules.
    Each neighbor is a complete schedule modification.
    """
    neighbors: List[List[Dict[str, Any]]] = []
    doctor_ids = [d.id for d in doctors]
    room_ids = [r.id for r in rooms]
    n = len(current_schedule)

    if n == 0:
        return []

    # -------------------------------------------------------------
    # 1. MOVE TIME OPERATOR: shift start time earlier or later
    # -------------------------------------------------------------
    time_shift_count = 0
    time_offsets = [-15, -10, -5, 5, 10, 15]

    for idx, appt in enumerate(current_schedule):
        patient = patients_dict.get(appt["patient_id"])
        if not patient:
            continue

        arrival = patient.arrival_time if isinstance(patient.arrival_time, int) else parse_time(patient.arrival_time)
        duration = appt["end_time"] - appt["start_time"]

        for offset in time_offsets:
            new_start = appt["start_time"] + offset
            new_end = new_start + duration

            # Must satisfy patient arrival time and hospital operating bounds
            if new_start >= max(arrival, work_day_start) and new_end <= work_day_end:
                neighbor = copy.deepcopy(current_schedule)
                neighbor[idx]["start_time"] = new_start
                neighbor[idx]["end_time"] = new_end
                neighbor[idx]["waiting_time"] = max(0, new_start - arrival)
                neighbors.append(neighbor)
                time_shift_count += 1
                if time_shift_count >= max_candidates_per_type:
                    break
        if time_shift_count >= max_candidates_per_type:
            break

    # -------------------------------------------------------------
    # 2. CHANGE DOCTOR OPERATOR: reassign patient to a different doctor
    # -------------------------------------------------------------
    doc_change_count = 0
    for idx, appt in enumerate(current_schedule):
        curr_doc_id = appt["doctor_id"]
        for target_doc_id in doctor_ids:
            if target_doc_id != curr_doc_id:
                neighbor = copy.deepcopy(current_schedule)
                neighbor[idx]["doctor_id"] = target_doc_id
                neighbors.append(neighbor)
                doc_change_count += 1
                if doc_change_count >= max_candidates_per_type:
                    break
        if doc_change_count >= max_candidates_per_type:
            break

    # -------------------------------------------------------------
    # 3. CHANGE ROOM OPERATOR: reassign patient to a different room
    # -------------------------------------------------------------
    room_change_count = 0
    for idx, appt in enumerate(current_schedule):
        curr_room_id = appt["room_id"]
        for target_room_id in room_ids:
            if target_room_id != curr_room_id:
                neighbor = copy.deepcopy(current_schedule)
                neighbor[idx]["room_id"] = target_room_id
                neighbors.append(neighbor)
                room_change_count += 1
                if room_change_count >= max_candidates_per_type:
                    break
        if room_change_count >= max_candidates_per_type:
            break

    # -------------------------------------------------------------
    # 4. SWAP OPERATOR: swap doctor & room (or times) between two patients
    # -------------------------------------------------------------
    swap_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            a1 = current_schedule[i]
            a2 = current_schedule[j]
            p1 = patients_dict.get(a1["patient_id"])
            p2 = patients_dict.get(a2["patient_id"])

            if not p1 or not p2:
                continue

            arr1 = p1.arrival_time if isinstance(p1.arrival_time, int) else parse_time(p1.arrival_time)
            arr2 = p2.arrival_time if isinstance(p2.arrival_time, int) else parse_time(p2.arrival_time)
            dur1 = p1.consultation_duration
            dur2 = p2.consultation_duration

            # Option 4a: Swap Doctor & Room at existing times
            neighbor_swap_res = copy.deepcopy(current_schedule)
            neighbor_swap_res[i]["doctor_id"] = a2["doctor_id"]
            neighbor_swap_res[i]["room_id"] = a2["room_id"]
            neighbor_swap_res[j]["doctor_id"] = a1["doctor_id"]
            neighbor_swap_res[j]["room_id"] = a1["room_id"]
            neighbors.append(neighbor_swap_res)
            swap_count += 1

            # Option 4b: Swap Time Slots if both arrival times permit
            if a2["start_time"] >= arr1 and a1["start_time"] >= arr2:
                if a2["start_time"] + dur1 <= work_day_end and a1["start_time"] + dur2 <= work_day_end:
                    neighbor_swap_time = copy.deepcopy(current_schedule)
                    neighbor_swap_time[i]["start_time"] = a2["start_time"]
                    neighbor_swap_time[i]["end_time"] = a2["start_time"] + dur1
                    neighbor_swap_time[i]["waiting_time"] = max(0, a2["start_time"] - arr1)

                    neighbor_swap_time[j]["start_time"] = a1["start_time"]
                    neighbor_swap_time[j]["end_time"] = a1["start_time"] + dur2
                    neighbor_swap_time[j]["waiting_time"] = max(0, a1["start_time"] - arr2)
                    neighbors.append(neighbor_swap_time)
                    swap_count += 1

            if swap_count >= max_candidates_per_type:
                break
        if swap_count >= max_candidates_per_type:
            break

    return neighbors
