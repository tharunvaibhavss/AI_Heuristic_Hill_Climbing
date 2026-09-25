# 1. Project Overview

## Project Title
**Hospital Patient Scheduling using Heuristic Function and Hill Climbing**

## Academic Problem Context
Patient consultation scheduling in outpatient clinics and hospitals is an NP-hard combinatorial optimization challenge. Managing a high influx of patients while balancing doctor availability, consultation room occupancy, patient arrival times, priority classifications, and personal doctor preferences creates an enormous solution space that defies brute-force enumeration.

In a clinical facility operating during a morning window (**09:00 AM to 01:00 PM** &mdash; 4 hours or 240 minutes), poor scheduling leads to:
1. Long and uncomfortable patient waiting times in waiting rooms.
2. Inadequate care for urgent, high-priority, or emergency cases.
3. Severe bottlenecks and idle periods for doctors.
4. Overcrowded or under-utilized physical examination rooms.
5. Inevitable double-booking conflicts where two patients are scheduled with the same doctor or in the same room simultaneously.

## Operational Parameters
The baseline benchmark system models a standard outpatient clinic session:
- **Daily Operating Window**: 09:00 AM &ndash; 01:00 PM (240 operational minutes)
- **Patient Cohort**: 20 registered patients with varied arrival timestamps (09:00 to 11:30), consultation requirements (10 to 30 minutes), triage priorities (`HIGH`, `MEDIUM`, `LOW`), and optional doctor preferences.
- **Medical Staff**: 4 doctors on duty from 09:00 to 13:00 (Dr. Sarah Jenkins, Dr. Robert Chen, Dr. Emily Patel, Dr. Marcus Vance). Total capacity: 960 doctor-minutes.
- **Physical Facilities**: 3 consultation rooms active from 09:00 to 13:00 (Room A-101, Room B-102, Room C-103). Total capacity: 720 room-minutes.

## Why a Heuristic Local Search Approach?
For 20 patients, each requiring an assignment of a start time (in 5-minute increments), a doctor (4 options), and a room (3 options), the number of permutations exceeds $10^{20}$. Exhaustive search would take hours or days and is impractical for daily clinical operations.

Instead, this project employs an **AI Heuristic Evaluation Function** coupled with **Best-Improvement Hill Climbing**:
1. A **Deterministic Greedy Initial Schedule** establishes an initial valid, conflict-free baseline by sorting patients by clinical urgency and earliest arrival, packing them into the earliest feasible slots.
2. An **Objective Cost Function** $H(S) = 5(WT) + 100(C) + 20(P) + 10(U)$ quantifies schedule quality across four competing objectives.
3. **Hill Climbing Local Search** systematically evaluates neighborhoods formed by shifting start times, reassigning doctors, reassigning rooms, or swapping patient slots to seek local improvements without requiring exhaustive search.
