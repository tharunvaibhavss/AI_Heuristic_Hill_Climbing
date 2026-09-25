# 14. System Limitations

While the system successfully addresses the assignment requirements and satisfies all constraints, the following realistic engineering and algorithmic limitations exist:

1. **Local Minimum Entrapment**:
   - Standard Hill Climbing is strictly downhill ($H(S') < H(S)$). If the initial greedy schedule is already at a local minimum with respect to the neighborhood operators, the search terminates immediately without exploring alternative basins of attraction.

2. **No Guarantee of Global Optimality**:
   - Because the search space is NP-hard and Hill Climbing does not accept uphill moves, there is no mathematical proof that $H(S) = 1047.7$ is the absolute global minimum among all $20!$ permutations.

3. **Fixed Operational Window**:
   - The current implementation assumes a fixed 4-hour morning session (09:00&ndash;13:00). It does not natively handle multi-shift or 24/7 hospital emergency operations.

4. **Single-Day Scope**:
   - Consultations cannot be deferred to subsequent clinic days.

5. **Uniform Doctor Competency**:
   - While patient doctor preferences are modeled, all doctors are treated as clinically qualified for all general consultations. Specialized sub-discipline constraints (e.g., cardiology vs orthopedics) are not enforced.

6. **Static Consultation Durations**:
   - Consultation durations are assumed deterministic (10 to 30 minutes) as specified in registration; clinical delays or procedure overruns during real-time appointments are not modeled dynamically.
