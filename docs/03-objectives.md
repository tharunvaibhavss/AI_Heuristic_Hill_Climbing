# 3. System Objectives

The primary academic and technical objectives of this project are:

1. **Minimize Total and Average Patient Waiting Time ($WT$)**:
   - Keep patient delay $t_{\text{start}} - t_{\text{arrival}}$ as low as possible across all priority tiers.
   - Benchmark target: Average waiting time below 15 minutes per patient for the 20-patient cohort.

2. **Guarantee Priority-Based Clinical Triage ($P$)**:
   - Schedule urgent `HIGH` priority cases with zero or minimal delay (target: 0 minutes wait).
   - Maintain `MEDIUM` priority wait times below 30 minutes.
   - Prevent triage inversions where lower-priority arrivals preempt waiting emergency patients without clinical cause.

3. **Maximize and Balance Doctor Resource Utilization**:
   - Ensure all 4 doctors are engaged proportionally without overloading individual clinicians while others remain idle.

4. **Maximize Consultation Room Occupancy**:
   - Achieve steady facility flow across all 3 consultation rooms throughout the 09:00&ndash;13:00 operational window.

5. **Strictly Prevent Resource Conflicts ($C = 0$)**:
   - Enforce hard temporal constraints so that no doctor or room is ever double-booked.
   - Penalize candidate conflicts heavily ($W_2 = 100$) so the search engine rejects infeasible configurations.

6. **Avoid Infeasible Combinatorial Enumeration**:
   - Deploy deterministic greedy construction and Best-Improvement Hill Climbing local search to produce high-quality schedules within sub-second latencies (&lt;500 ms).
