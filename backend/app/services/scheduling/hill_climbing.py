"""
Hill Climbing Local Search Optimization Engine for Hospital Patient Scheduling.

Strategy:
- Best-Improvement Hill Climbing
- Strictly accepts: new_score < current_score
- Rejects: new_score >= current_score
- Stops when no neighbor provides improvement (local minimum) or max iterations reached.
"""

import logging
from typing import List, Dict, Any, Optional
from app.services.scheduling.heuristic import calculate_heuristic
from app.services.scheduling.neighbors import generate_neighbors

logger = logging.getLogger("scheduling.hill_climbing")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

MAX_ITERATIONS_DEFAULT = 1000

def hill_climb(
    initial_schedule: List[Dict[str, Any]],
    patients: List[Any],
    doctors: List[Any],
    rooms: List[Any],
    max_iterations: int = MAX_ITERATIONS_DEFAULT
) -> Dict[str, Any]:
    """
    Executes the Best-Improvement Hill Climbing local search optimization.

    Returns:
        A dictionary with initial_score, final_score, iterations, improvement,
        heuristic breakdown, and final optimized schedule.
    """
    patients_dict = {p.id: p for p in patients}
    doctors_dict = {d.id: d for d in doctors}
    rooms_dict = {r.id: r for r in rooms}

    current_schedule = [dict(appt) for appt in initial_schedule]
    initial_eval = calculate_heuristic(current_schedule, patients_dict, doctors_dict, rooms_dict)
    current_score = initial_eval["total_score"]
    current_eval = initial_eval

    logger.info(
        f"Starting Hill Climbing: Initial H(S)={current_score} "
        f"(WT={initial_eval['waiting_time']}, C={initial_eval['conflicts']}, "
        f"P={initial_eval['priority_penalty']}, U={initial_eval['under_utilization']})"
    )

    iteration = 0
    total_evaluations = 0

    while iteration < max_iterations:
        candidate_neighbors = generate_neighbors(
            current_schedule,
            patients_dict,
            doctors,
            rooms
        )

        if not candidate_neighbors:
            logger.info(f"No candidate neighbors generated at iteration {iteration + 1}. Terminating.")
            break

        total_evaluations += len(candidate_neighbors)
        best_neighbor: Optional[List[Dict[str, Any]]] = None
        best_neighbor_score = current_score
        best_neighbor_eval: Optional[Dict[str, Any]] = None

        # Evaluate all generated neighbors (Best-Improvement)
        for neighbor in candidate_neighbors:
            eval_res = calculate_heuristic(neighbor, patients_dict, doctors_dict, rooms_dict)
            neighbor_score = eval_res["total_score"]

            if neighbor_score < best_neighbor_score:
                best_neighbor_score = neighbor_score
                best_neighbor = neighbor
                best_neighbor_eval = eval_res

        # Strictly accept only if strictly lower heuristic score
        if best_neighbor is not None and best_neighbor_score < current_score:
            improvement = round(current_score - best_neighbor_score, 2)
            logger.info(
                f"Iteration {iteration + 1}: Accepted neighbor! "
                f"Score improved: {current_score} -> {best_neighbor_score} (Delta: -{improvement})"
            )
            current_schedule = best_neighbor
            current_score = best_neighbor_score
            current_eval = best_neighbor_eval
            iteration += 1
        else:
            logger.info(
                f"Iteration {iteration + 1}: No better neighbor found (best candidate score: {best_neighbor_score}, "
                f"current score: {current_score}). Local minimum reached. Terminating."
            )
            break

    total_improvement = round(initial_eval["total_score"] - current_score, 2)
    status_message = (
        "No improving neighbor found. Hill Climbing stopped at a local minimum."
        if iteration == 0
        else f"Optimized via {iteration} accepted moves. Local minimum reached."
    )

    logger.info(
        f"Hill Climbing completed: {iteration} iterations, "
        f"Evaluations={total_evaluations}, "
        f"Initial Score={initial_eval['total_score']} -> Final Score={current_score} "
        f"(Total Improvement={total_improvement})"
    )

    return {
        "initial_schedule": initial_schedule,
        "final_schedule": current_schedule,
        "initial_score": initial_eval["total_score"],
        "final_score": current_score,
        "iterations": iteration,
        "improvement": total_improvement,
        "accepted_moves": iteration,
        "neighbor_evaluations": total_evaluations,
        "status_message": status_message,
        "heuristic": current_eval
    }

