# 9. Hill Climbing Algorithm & Local Search

## Algorithm Strategy: Best-Improvement Hill Climbing
Hill Climbing is a local search trajectory heuristic that explores adjacent configurations in a neighborhood space $\mathcal{N}(S)$.

```text
Algorithm: Best-Improvement Hill Climbing
Input: Initial Schedule S0, Objective Function H(S)
Output: Locally Optimized Schedule S_final

1. S_current <- S0
2. current_score <- H(S_current)
3. loop:
4.     candidate_neighbors <- GenerateNeighbors(S_current)
5.     if candidate_neighbors is empty:
6.         break
7.     best_neighbor <- None
8.     best_score <- current_score
9.     for each neighbor S' in candidate_neighbors:
10.        score' <- H(S')
11.        if score' < best_score:
12.            best_score <- score'
13.            best_neighbor <- S'
14.    if best_neighbor is not None and best_score < current_score:
15.        S_current <- best_neighbor
16.        current_score <- best_score
17.    else:
18.        break (Local minimum reached: No neighbor strictly improves score)
19. return S_current
```

## Neighborhood Generation Operators
The neighborhood generator (`backend/app/services/scheduling/neighbors.py`) produces up to 100 candidate neighbor states across 4 distinct operators:
1. **Move Time Operator**: Shifts a patient's consultation start time earlier or later by $\pm 10$ minutes (subject to operational bounds and patient arrival times).
2. **Reassign Doctor Operator**: Changes a patient's assigned clinician to an alternate doctor while preserving start time and room.
3. **Reassign Room Operator**: Moves an appointment to an alternate consultation room while preserving start time and doctor.
4. **Swap Patients Operator**: Exchanges assigned slots (time, doctor, room) between two patients.

## Empirical Behavior & Local Minimum Analysis
In our benchmark run:
- **Initial Score $H(S_0)$**: $1047.7$
- **Candidate Neighbors Evaluated**: $100$
- **Accepted Moves**: $0$
- **Final Score $H(S_{\text{final}})$**: $1047.7$
- **Termination Reason**: Local minimum reached.

### Why Did Hill Climbing Accept 0 Moves?
1. The deterministic initial schedule generator already constructed a highly optimized, compact schedule that scheduled all 20 patients without conflicts ($C=0$), accommodated all 5 `HIGH` priority patients with 0 minutes wait, and packed consultations tightly.
2. Every 1-step perturbation in the neighborhood either:
   - Increased waiting time $WT$,
   - Introduced a hard overlap conflict ($C > 0$), adding $+100$ points to $H(S)$,
   - Or caused an unfavorable priority delay.
3. Therefore, no candidate neighbor satisfied $H(S') < 1047.7$.
4. **Academic Clarification**: Zero accepted moves demonstrates that the initial greedy state was already a **local minimum** with respect to the defined neighborhood. It does not represent algorithmic failure, nor does it guarantee a global optimum over all possible combinatorial states.
