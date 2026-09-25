# 10. End-to-End Scheduling Workflow

## Workflow Architecture Diagram

```text
               [ Registered Patient Cohort ]
               (Arrivals, Durations, Priorities)
                              |
                              v
             +----------------------------------+
             |   Priority Sorting & Ordering    |
             |   1. Priority (HIGH > MED > LOW) |
             |   2. Arrival Time (Earliest First|
             +----------------------------------+
                              |
                              v
             +----------------------------------+
             | Greedy Earliest Feasible Slot    |
             | - Query preferred doctor         |
             | - Query alternative doctors      |
             | - Find earliest available room   |
             +----------------------------------+
                              |
                              v
                  [ Initial Schedule S0 ]
                      H(S0) = 1047.7
                              |
                              v
             +----------------------------------+
             |   Neighborhood State Generator   |
             |  - Move Time (+-10m)             |
             |  - Reassign Doctor               |
             |  - Reassign Room                 |
             |  - Swap Patients                 |
             +----------------------------------+
                              |
                              v
             +----------------------------------+
             |   Heuristic Evaluator (100 Evals)|
             |   Compute H(S') = 5WT+100C+20P+10U|
             +----------------------------------+
                              |
                              v
                   [ Is H(S') < H(S)? ]
                      /             \
                    YES              NO
                    /                 \
       [ Accept Best Neighbor ]   [ STOP: Local Minimum ]
                    |                          |
             (Next Iteration)                  v
                                    [ Final Schedule S_final ]
                                               |
                                               v
                                    [ Atomic SQLite Commit ]
                                               |
                                               v
                                    [ Render in Next.js UI ]
```
