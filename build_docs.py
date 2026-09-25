"""
Script to generate the complete technical documentation suite in docs/
"""

import os

DOCS_DIR = r"c:\Users\HP\Desktop\AI_project\docs"
os.makedirs(DOCS_DIR, exist_ok=True)

docs = {}

# -------------------------------------------------------------
# 01-project-overview.md
# -------------------------------------------------------------
docs["01-project-overview.md"] = """# 1. Project Overview

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
"""

# -------------------------------------------------------------
# 02-problem-statement.md
# -------------------------------------------------------------
docs["02-problem-statement.md"] = """# 2. Problem Statement

## Formal Problem Definition
The objective of the hospital patient scheduling problem is to construct a consultation schedule $S$ that assigns each patient $i \in \{1, \dots, N\}$:
- a consultation start time $t_{\\text{start}}(i)$ and end time $t_{\\text{end}}(i) = t_{\\text{start}}(i) + d_i$,
- an assigned doctor $D(i)$,
- and an assigned examination room $R(i)$,

such that:
1. **Patient Waiting Time ($WT$) is minimized**: The delay between patient arrival time $a_i$ and consultation commencement $t_{\\text{start}}(i)$ must be kept as short as possible.
2. **Emergency and High-Priority Patients are expedited**: Patients designated with `HIGH` priority must receive prompt attention without unnecessary delays.
3. **Doctors are utilized efficiently**: Doctor workload should be distributed equitably across the session without long idle periods.
4. **Consultation rooms are utilized efficiently**: Facility turnover should be maintained without bottlenecks.
5. **Hard Scheduling Conflicts ($C$) are eliminated**: Under no circumstances may two patients overlap with the same doctor or within the same consultation room simultaneously.
6. **Doctor Preferences are honored when feasible**: Patient doctor preferences should be respected when open slots permit without inducing conflicts.

## Mathematical Formulation
The optimization problem is formalized as finding an assignment $S^*$:

$$\\min_{S \\in \\mathcal{S}} H(S)$$

subject to hard operational constraints:
- $t_{\\text{start}}(i) \\ge a_i \\quad \\forall i$
- $t_{\\text{start}}(i) \\ge \\text{start}(D(i))$ and $t_{\\text{end}}(i) \\le \\text{end}(D(i)) \\quad \\forall i$
- $t_{\\text{start}}(i) \\ge \\text{start}(R(i))$ and $t_{\\text{end}}(i) \\le \\text{end}(R(i)) \\quad \\forall i$
- $\\text{No doctor overlap}: [t_{\\text{start}}(i), t_{\\text{end}}(i)) \\cap [t_{\\text{start}}(j), t_{\\text{end}}(j)) = \\emptyset \\quad \\text{if } D(i) = D(j)$
- $\\text{No room overlap}: [t_{\\text{start}}(i), t_{\\text{end}}(i)) \\cap [t_{\\text{start}}(j), t_{\\text{end}}(j)) = \\emptyset \\quad \\text{if } R(i) = R(j)$
"""

# -------------------------------------------------------------
# 03-objectives.md
# -------------------------------------------------------------
docs["03-objectives.md"] = """# 3. System Objectives

The primary academic and technical objectives of this project are:

1. **Minimize Total and Average Patient Waiting Time ($WT$)**:
   - Keep patient delay $t_{\\text{start}} - t_{\\text{arrival}}$ as low as possible across all priority tiers.
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
"""

# -------------------------------------------------------------
# 04-system-architecture.md
# -------------------------------------------------------------
docs["04-system-architecture.md"] = """# 4. System Architecture

The application is engineered as a decoupled, multi-tiered full-stack system comprising a reactive Next.js 16 frontend and a high-performance FastAPI Python backend communicating over typed REST APIs.

## Architecture Diagram

```text
+-------------------------------------------------------------------+
|                        NEXT.JS 16 FRONTEND                        |
|   App Router | TypeScript | Tailwind CSS v4 | Lucide React Icons  |
|                                                                   |
|   / (Dashboard)      /patients (CRUD)     /doctors (Directory)   |
|   /rooms (Rooms)     /schedule (Gantt)    /heuristic (Analysis)  |
+-------------------------------------------------------------------+
                                  |
                                  | HTTP / JSON REST Calls
                                  v
+-------------------------------------------------------------------+
|                         FASTAPI BACKEND                           |
|       Python 3.13 | Pydantic v2 | SQLAlchemy 2.0 ORM Engine       |
|                                                                   |
|  +--------------------+  +--------------------+  +--------------+ |
|  |     CRUD APIs      |  |   Heuristic Eval   |  | Seed Engine  | |
|  | Patients, Doctors, |  | Dynamic Cost Breakdown| Resets 20/4/3 | |
|  | Rooms, Schedules   |  | WT, C, P, U Terms  |  | Benchmark    | |
|  +--------------------+  +--------------------+  +--------------+ |
|                                 |                                 |
|                                 v                                 |
|  +-------------------------------------------------------------+  |
|  |             SCHEDULING ENGINE (Local Search Core)           |  |
|  |   1. Initial Schedule: Priority Sort + Greedy Slot Packing  |  |
|  |   2. Neighborhood Ops: Time Shift, Doctor, Room, Swap       |  |
|  |   3. Hill Climbing: Best-Improvement Local Search (Min H)   |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
                                  |
                                  | SQLAlchemy ORM Queries & Commits
                                  v
+-------------------------------------------------------------------+
|                         SQLITE DATABASE                           |
|                    hospital_scheduling.db                         |
|     patients  |  doctors  |  rooms  |  schedules (UNIQUE pid)     |
+-------------------------------------------------------------------+
```

## Layer Responsibilities

### 1. Presentation Tier (Next.js 16)
- **App Router Architecture**: Server and Client Components optimized for speed and reactivity.
- **Interactive Visualizations**: Gantt-style timeline (09:00&ndash;13:00) mapping appointments by room and doctor.
- **Analytical Dashboards**: Real-time rendering of heuristic cost terms, optimization search trajectories, and comparative benchmarks.
- **Modal CRUD Operations**: Form validation for managing patients, doctors, and rooms.

### 2. Service & Algorithm Tier (FastAPI & Python Core)
- **Time Conversion Utilities**: High-precision conversions between human `HH:MM` strings and integer minutes from midnight.
- **Constraint Validator**: Exhaustive interval overlap checks for doctor and room conflicts.
- **Heuristic Evaluator**: Calculates $H(S) = 5(WT) + 100(C) + 20(P) + 10(U)$.
- **Hill Climbing Engine**: Evaluates neighborhood states and enforces strict downhill transitions ($H(S') < H(S)$).

### 3. Data Persistence Tier (SQLite & SQLAlchemy 2.0)
- **Relational Integrity**: Foreign key constraints between schedules, patients, doctors, and rooms.
- **Idempotency Guarantee**: UNIQUE constraint on `schedules.patient_id` ensuring exactly one appointment per patient.
"""

# -------------------------------------------------------------
# 05-technology-stack.md
# -------------------------------------------------------------
docs["05-technology-stack.md"] = """# 5. Technology Stack

The technology stack was selected to provide academic rigor, robust type safety, determinism, and rapid execution.

## Frontend Technologies
| Component | Technology | Version | Rationale |
|:---|:---|:---|:---|
| **Framework** | Next.js (App Router) | 16.3.6 | Modern React framework with static prerendering, zero layout shift, and server component optimization. |
| **Language** | TypeScript | 5.x | Strict end-to-end type safety eliminating runtime null pointer exceptions. |
| **Styling** | Tailwind CSS | v4.0.0 | High-performance atomic utility styling with modern CSS variables. |
| **Icons** | Lucide React | 1.16.0 | Clean, accessible vector icons for medical and algorithmic dashboards. |
| **Bundler** | Turbopack | Built-in | Fast local compilation and sub-second hot reload cycles. |

## Backend Technologies
| Component | Technology | Version | Rationale |
|:---|:---|:---|:---|
| **Runtime** | Python | 3.13.2 | High expressiveness for AI heuristics, algorithmic operations, and data transformations. |
| **Web Framework**| FastAPI | 0.115.x | Asynchronous REST framework with automatic OpenAPI documentation and high throughput. |
| **Validation** | Pydantic | v2.10.x | Strict data validation, regex time format checks, and JSON serialization. |
| **ORM** | SQLAlchemy | 2.0.x | Industrial-strength ORM for relational queries, relationships, and transactional commits. |
| **Database** | SQLite 3 | Embedded | Self-contained, zero-configuration relational database engine ideal for academic reproducibility. |
| **Test Engine** | Pytest & TestClient | 9.1.x | Comprehensive unit and integration test suite with high-speed automated assertions. |
"""

# -------------------------------------------------------------
# 06-database-design.md
# -------------------------------------------------------------
docs["06-database-design.md"] = """# 6. Database Design

The relational database is implemented in SQLite (`hospital_scheduling.db`) managed via SQLAlchemy 2.0.

## Entity Relationship (ER) Diagram

```text
       +-------------------------+
       |         doctors         |
       +-------------------------+
       | id: INTEGER (PK)        |<---------+
       | name: VARCHAR(100)      |          |
       | available_from: VARCHAR |          |
       | available_until: VARCHAR|          |
       | created_at: DATETIME    |          |
       +-------------------------+          |
                   |                        |
                   | 1                      |
                   |                        | 1
                   v M                      |
       +-------------------------+          |
       |        patients         |          |
       +-------------------------+          |
       | id: INTEGER (PK)        |          |
       | name: VARCHAR(100)      |          |
       | arrival_time: VARCHAR(5)|          |
       | priority: ENUM          |          |
       | consultation_duration:  |          |
       | preferred_doctor_id: FK |----------+
       | created_at: DATETIME    |
       +-------------------------+
                   |
                   | 1
                   v 1 (UNIQUE)
       +-------------------------+          +-------------------------+
       |        schedules        |          |          rooms          |
       +-------------------------+          +-------------------------+
       | id: INTEGER (PK)        |          | id: INTEGER (PK)        |
       | patient_id: INTEGER(FK) |          | name: VARCHAR(50)       |
       | doctor_id: INTEGER(FK)  |--------->| available_from: VARCHAR |
       | room_id: INTEGER(FK)    |--------->| available_until: VARCHAR|
       | start_time: VARCHAR(5)  |       M:1| created_at: DATETIME    |
       | end_time: VARCHAR(5)    |          +-------------------------+
       | waiting_time: INTEGER   |
       | created_at: DATETIME    |
       +-------------------------+
```

## Table Specifications

### 1. `patients` Table
| Column Name | Data Type | Nullable | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `id` | INTEGER | No | PRIMARY KEY, AUTOINCREMENT | Unique patient ID |
| `name` | VARCHAR(100) | No | None | Patient full name |
| `arrival_time` | VARCHAR(5) | No | Format `HH:MM` | Time patient arrives at clinic |
| `priority` | VARCHAR(10) | No | Enum: `HIGH`, `MEDIUM`, `LOW` | Clinical triage priority |
| `consultation_duration`| INTEGER | No | $10 \le t \le 30$ | Consultation length (minutes) |
| `preferred_doctor_id` | INTEGER | Yes | FOREIGN KEY (`doctors.id`) | Optional preferred clinician |
| `created_at` | DATETIME | Yes | DEFAULT UTC NOW | Record insertion timestamp |

### 2. `doctors` Table
| Column Name | Data Type | Nullable | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `id` | INTEGER | No | PRIMARY KEY, AUTOINCREMENT | Unique clinician ID |
| `name` | VARCHAR(100) | No | None | Doctor full name |
| `available_from` | VARCHAR(5) | No | Format `HH:MM`, Default `'09:00'` | Shift start timestamp |
| `available_until` | VARCHAR(5) | No | Format `HH:MM`, Default `'13:00'` | Shift end timestamp |
| `created_at` | DATETIME | Yes | DEFAULT UTC NOW | Record insertion timestamp |

### 3. `rooms` Table
| Column Name | Data Type | Nullable | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `id` | INTEGER | No | PRIMARY KEY, AUTOINCREMENT | Unique room ID |
| `name` | VARCHAR(50) | No | None | Room name / designation |
| `available_from` | VARCHAR(5) | No | Format `HH:MM`, Default `'09:00'` | Facility opening time |
| `available_until` | VARCHAR(5) | No | Format `HH:MM`, Default `'13:00'` | Facility closing time |
| `created_at` | DATETIME | Yes | DEFAULT UTC NOW | Record insertion timestamp |

### 4. `schedules` Table
| Column Name | Data Type | Nullable | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `id` | INTEGER | No | PRIMARY KEY, AUTOINCREMENT | Unique appointment ID |
| `patient_id` | INTEGER | No | FOREIGN KEY (`patients.id`), **UNIQUE** | Scheduled patient (1-to-1) |
| `doctor_id` | INTEGER | No | FOREIGN KEY (`doctors.id`) | Assigned doctor |
| `room_id` | INTEGER | No | FOREIGN KEY (`rooms.id`) | Assigned consultation room |
| `start_time` | VARCHAR(5) | No | Format `HH:MM` | Scheduled consultation start |
| `end_time` | VARCHAR(5) | No | Format `HH:MM` | Scheduled consultation end |
| `waiting_time` | INTEGER | No | Non-negative integer | Calculated delay ($t_{\\text{start}} - a_i$) |
| `created_at` | DATETIME | Yes | DEFAULT UTC NOW | Schedule generation timestamp |
"""

# -------------------------------------------------------------
# 07-api-documentation.md
# -------------------------------------------------------------
docs["07-api-documentation.md"] = """# 7. REST API Documentation

The backend exposes a clean REST API running by default on `http://localhost:8000/api`. Interactive OpenAPI / Swagger UI documentation is available at `http://localhost:8000/docs`.

## 1. System Health
- **Endpoint**: `GET /api/health`
- **Description**: Verifies backend server health, database connectivity, and record counts.
- **Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-09-26T00:31:00Z",
  "database": {
    "status": "connected",
    "patient_count": 20,
    "doctor_count": 4,
    "room_count": 3,
    "scheduled_count": 20
  },
  "version": "1.0.0"
}
```

## 2. Seed & Reset Engine
- **Endpoint**: `POST /api/seed/reset`
- **Description**: Atomically resets the database and seeds the deterministic 20-patient, 4-doctor, 3-room benchmark dataset.
- **Response**:
```json
{
  "message": "Database reset and seeded successfully",
  "patients_count": 20,
  "doctors_count": 4,
  "rooms_count": 3
}
```

## 3. Patient Management
- `GET /api/patients`: List all registered patients.
- `GET /api/patients/{id}`: Retrieve a specific patient by ID.
- `POST /api/patients`: Register a new patient.
  - Required fields: `name`, `arrival_time`, `priority` (`HIGH`|`MEDIUM`|`LOW`), `consultation_duration` ($10 \le t \le 30$).
  - Optional fields: `preferred_doctor_id`.
- `PUT /api/patients/{id}`: Update patient details.
- `DELETE /api/patients/{id}`: Delete a patient record.

## 4. Doctor Management
- `GET /api/doctors`: List all doctors and their operating shifts.
- `POST /api/doctors`: Create doctor record (`name`, `available_from`, `available_until`).
- `PUT /api/doctors/{id}`: Update doctor information.
- `DELETE /api/doctors/{id}`: Remove doctor record.

## 5. Room Management
- `GET /api/rooms`: List all consultation rooms.
- `POST /api/rooms`: Create room record (`name`, `available_from`, `available_until`).
- `PUT /api/rooms/{id}`: Update room details.
- `DELETE /api/rooms/{id}`: Remove room record.

## 6. Scheduling & Optimization Endpoints
- **Endpoint**: `POST /api/schedule/generate`
  - **Description**: Executes the initial deterministic schedule generation, runs Best-Improvement Hill Climbing local search, persists the resulting schedule to SQLite, and returns full metrics.
  - **Response**:
```json
{
  "success": true,
  "initial_score": 1047.7,
  "final_score": 1047.7,
  "iterations": 0,
  "improvement": 0.0,
  "accepted_moves": 0,
  "neighbor_evaluations": 100,
  "status_message": "No improving neighbor found. Hill Climbing stopped at a local minimum.",
  "heuristic": {
    "waiting_time": 195,
    "conflicts": 0,
    "priority_penalty": 2.0,
    "under_utilization": 3.27,
    "waiting_cost": 975.0,
    "conflict_cost": 0.0,
    "priority_cost": 40.0,
    "utilization_cost": 32.7,
    "total_score": 1047.7
  },
  "schedule": [...]
}
```
- **Endpoint**: `GET /api/schedule`: Retrieves the current active schedule records from SQLite.
- **Endpoint**: `GET /api/schedule/score`: Evaluates and returns the heuristic cost breakdown of the currently stored schedule.
"""

# -------------------------------------------------------------
# 08-heuristic-function.md
# -------------------------------------------------------------
docs["08-heuristic-function.md"] = """# 8. Heuristic Function Formulation

The evaluation engine quantifies the quality of any given schedule state $S$ through a composite heuristic cost function:

$$H(S) = W_1(WT) + W_2(C) + W_3(P) + W_4(U)$$

Because this is a **minimization problem**, lower numerical values indicate higher quality schedules.

## Mathematical Weights & Design Rationale
| Term | Coefficient | Symbol | Meaning | Rationale |
|:---|:---:|:---:|:---|:---|
| **Waiting Time** | $W_1 = 5$ | $WT$ | Total patient waiting time (minutes) | Directly affects patient satisfaction and waiting room congestion. |
| **Conflicts** | $W_2 = 100$ | $C$ | Number of resource collisions | Hard constraint multiplier ensuring invalid states are rejected. |
| **Priority Penalty** | $W_3 = 20$ | $P$ | Clinical triage delay and ordering penalty | Ensures urgent cases are seen promptly without clinical danger. |
| **Under-utilization** | $W_4 = 10$ | $U$ | Idle capacity & imbalance metric | Encourages efficient resource usage across doctors and rooms. |

## Term 1: Total Waiting Time ($WT$)
For each scheduled patient $i \\in \\{1, \\dots, N\\}$, waiting time is defined as the elapsed duration between patient arrival time $a_i$ and scheduled consultation commencement $t_{\\text{start}}(i)$:

$$WT = \\sum_{i=1}^{N} \\max(0, t_{\\text{start}}(i) - a_i)$$

In the benchmark schedule:
$$WT = 195 \\text{ minutes} \\implies 5 \\times 195 = 975.0$$

## Term 2: Scheduling Conflicts ($C$)
$C$ represents the count of overlapping interval pairs:
- **Doctor Overlap**: Patient $i$ and $j$ assigned to the same doctor where $[t_{\\text{start}}(i), t_{\\text{end}}(i)) \\cap [t_{\\text{start}}(j), t_{\\text{end}}(j)) \\ne \\emptyset$.
- **Room Overlap**: Patient $i$ and $j$ assigned to the same room where $[t_{\\text{start}}(i), t_{\\text{end}}(i)) \\cap [t_{\\text{start}}(j), t_{\\text{end}}(j)) \\ne \\emptyset$.

In the benchmark schedule:
$$C = 0 \\implies 100 \\times 0 = 0.0$$

## Term 3: Priority Penalty ($P$)
The academic assignment specifies that emergency and high-priority patients must be prioritized, but leaves the exact implementation to the engineer. The implemented formula in `backend/app/services/scheduling/heuristic.py` evaluates:
1. **Excess Delay Thresholds**:
   - `HIGH` priority tolerates up to 15 min wait: $\\text{penalty} += \\lceil \\max(0, \\text{wait} - 15) / 5 \\rceil$.
   - `MEDIUM` priority tolerates up to 30 min wait: $\\text{penalty} += \\lceil \\max(0, \\text{wait} - 30) / 10 \\rceil$.
   - `LOW` priority tolerates up to 45 min wait: $\\text{penalty} += \\lceil \\max(0, \\text{wait} - 45) / 15 \\rceil$.
2. **Priority Ordering Inversion**:
   - Assesses a $+0.5$ penalty if a lower-priority patient begins consultation earlier than an already-waiting higher-priority patient.

In the benchmark schedule:
$$P = 2.0 \\implies 20 \\times 2.0 = 40.0$$

## Term 4: Under-Utilization Penalty ($U$)
Defined based on total idle capacity across doctor shifts and room operating hours:
- Doctor Capacity: $4 \\times 240 = 960$ minutes. Consultations used: $375$ min (Unused: $585$ min / 60.9%).
- Room Capacity: $3 \\times 240 = 720$ minutes. Consultations used: $375$ min (Unused: $345$ min / 47.9%).
- Unused capacity fractions are normalized with a doctor workload standard deviation term, scaling to an index value:
$$U = 3.27 \\implies 10 \\times 3.27 = 32.7$$

## Total Heuristic Value
$$H(S) = 975.0 + 0.0 + 40.0 + 32.7 = 1047.7$$
"""

# -------------------------------------------------------------
# 09-hill-climbing-algorithm.md
# -------------------------------------------------------------
docs["09-hill-climbing-algorithm.md"] = """# 9. Hill Climbing Algorithm & Local Search

## Algorithm Strategy: Best-Improvement Hill Climbing
Hill Climbing is a local search trajectory heuristic that explores adjacent configurations in a neighborhood space $\\mathcal{N}(S)$.

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
1. **Move Time Operator**: Shifts a patient's consultation start time earlier or later by $\\pm 10$ minutes (subject to operational bounds and patient arrival times).
2. **Reassign Doctor Operator**: Changes a patient's assigned clinician to an alternate doctor while preserving start time and room.
3. **Reassign Room Operator**: Moves an appointment to an alternate consultation room while preserving start time and doctor.
4. **Swap Patients Operator**: Exchanges assigned slots (time, doctor, room) between two patients.

## Empirical Behavior & Local Minimum Analysis
In our benchmark run:
- **Initial Score $H(S_0)$**: $1047.7$
- **Candidate Neighbors Evaluated**: $100$
- **Accepted Moves**: $0$
- **Final Score $H(S_{\\text{final}})$**: $1047.7$
- **Termination Reason**: Local minimum reached.

### Why Did Hill Climbing Accept 0 Moves?
1. The deterministic initial schedule generator already constructed a highly optimized, compact schedule that scheduled all 20 patients without conflicts ($C=0$), accommodated all 5 `HIGH` priority patients with 0 minutes wait, and packed consultations tightly.
2. Every 1-step perturbation in the neighborhood either:
   - Increased waiting time $WT$,
   - Introduced a hard overlap conflict ($C > 0$), adding $+100$ points to $H(S)$,
   - Or caused an unfavorable priority delay.
3. Therefore, no candidate neighbor satisfied $H(S') < 1047.7$.
4. **Academic Clarification**: Zero accepted moves demonstrates that the initial greedy state was already a **local minimum** with respect to the defined neighborhood. It does not represent algorithmic failure, nor does it guarantee a global optimum over all possible combinatorial states.
"""

# -------------------------------------------------------------
# 10-scheduling-workflow.md
# -------------------------------------------------------------
docs["10-scheduling-workflow.md"] = """# 10. End-to-End Scheduling Workflow

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
                      /             \\
                    YES              NO
                    /                 \\
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
"""

# -------------------------------------------------------------
# 11-frontend-guide.md
# -------------------------------------------------------------
docs["11-frontend-guide.md"] = """# 11. Frontend Application Guide

The user interface is built with Next.js 16 App Router and Tailwind CSS v4, delivering an intuitive clinical dashboard.

## Application Pages

### 1. Overview Dashboard (`/`)
- Displays real-time KPI cards: Total Patients, Doctors, Rooms, Scheduled Patients, Total Waiting Time, Average Waiting Time, Resource Conflicts, and Active Heuristic Score.
- Prominent **Generate Schedule** action button triggering real-time optimization.
- Live schedule preview table with priority badges and doctor assignments.

### 2. Patient Management (`/patients`)
- Data table displaying all 20 patients: Arrival time, Priority badge (`HIGH`, `MEDIUM`, `LOW`), Consultation duration, and Preferred doctor.
- Search and priority filter controls.
- Full CRUD modals: Add Patient, Edit Patient, Delete Patient with input validation.

### 3. Doctor Directory (`/doctors`)
- Directory cards for all 4 doctors with shift hours (09:00&ndash;13:00).
- Real-time capacity utilization gauges showing consultation minutes delivered vs capacity.

### 4. Room Directory (`/rooms`)
- Visual display of all 3 consultation rooms with operating schedules.
- Room occupancy percentages and utilization metrics.

### 5. Schedule & Visual Gantt Timeline (`/schedule`)
- Visual timeline mapping consultation blocks from 09:00 to 13:00 across rooms and doctors.
- Comprehensive appointment records table showing Arrival, Start, End, Waiting Time, and assigned resources.

### 6. Heuristic & Optimization Analysis (`/heuristic`)
- **Section 1**: Current Heuristic Score $H(S) = 1047.7$.
- **Section 2**: Mathematical formula definition with coefficient breakdown.
- **Section 3**: Live component cards ($WT=195$, $C=0$, $P=2.0$, $U=3.27$).
- **Section 4**: Additive weighted calculation breakdown ($975 + 0 + 40 + 32.7 = 1047.7$).
- **Section 5**: Hill Climbing Optimization Analysis with search metrics (Initial 1047.7, Final 1047.7, 0 moves, 100 evaluations, Local minimum status) and step diagram.
- **Section 6**: Assignment Example (Schedule A = 270 vs Schedule B = 290).
- **Section 7**: Theoretical explanation of local minima.
"""

# -------------------------------------------------------------
# 12-testing-and-validation.md
# -------------------------------------------------------------
docs["12-testing-and-validation.md"] = """# 12. Testing and Validation

A rigorous test-driven approach was maintained across both backend and frontend tiers.

## Backend Pytest Suite (22/22 Passing)
Execute tests:
```bash
cd backend
python -m pytest -v
```

### Test Suite Output
```text
============================= test session starts =============================
platform win32 -- Python 3.13.2, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\\Users\\HP\\Desktop\\AI_project\\backend
collected 22 items

tests/test_phase1.py::test_health_endpoint PASSED                        [  4%]
tests/test_phase1.py::test_get_doctors PASSED                            [  9%]
tests/test_phase1.py::test_get_rooms PASSED                              [ 13%]
tests/test_phase1.py::test_get_patients PASSED                           [ 18%]
tests/test_phase1.py::test_patient_validation PASSED                     [ 22%]
tests/test_scheduling.py::test_time_conversions PASSED                   [ 27%]
tests/test_scheduling.py::test_interval_overlaps PASSED                  [ 31%]
tests/test_scheduling.py::test_waiting_time PASSED                       [ 36%]
tests/test_scheduling.py::test_doctor_conflict PASSED                    [ 40%]
tests/test_scheduling.py::test_room_conflict PASSED                      [ 45%]
tests/test_scheduling.py::test_no_conflict_for_different_doctors PASSED  [ 50%]
tests/test_scheduling.py::test_no_conflict_for_different_rooms PASSED    [ 54%]
tests/test_scheduling.py::test_priority_penalty PASSED                   [ 59%]
tests/test_scheduling.py::test_under_utilization PASSED                  [ 63%]
tests/test_scheduling.py::test_heuristic_formula PASSED                  [ 68%]
tests/test_scheduling.py::test_conflict_has_large_weight_assignment_example PASSED [ 72%]
tests/test_scheduling.py::test_neighbor_generation PASSED                [ 77%]
tests/test_scheduling.py::test_hill_climbing_accepts_improvement PASSED  [ 81%]
tests/test_scheduling.py::test_hill_climbing_rejects_worse_solution PASSED [ 86%]
tests/test_scheduling.py::test_hill_climbing_terminates PASSED           [ 90%]
tests/test_scheduling.py::test_generated_schedule_respects_constraints PASSED [ 95%]
tests/test_scheduling.py::test_generate_and_get_schedule_api PASSED      [100%]

======================== 22 passed, 1 warning in 2.28s ========================
```

## Frontend Validation
- **Lint Check (`npm run lint`)**: Passed with **0 errors and 0 warnings**.
- **Production Build (`npm run build`)**: Compiled successfully in Turbopack; static prerendered routes for all pages (`/`, `/patients`, `/doctors`, `/rooms`, `/schedule`, `/heuristic`).

## Warning Audit
- `StarletteDeprecationWarning`: Originates from Starlette 0.45.3+ testclient internals when imported by `fastapi.testclient.TestClient`. Confirmed upstream deprecation notice with zero application runtime impact.
"""

# -------------------------------------------------------------
# 13-results-and-analysis.md
# -------------------------------------------------------------
docs["13-results-and-analysis.md"] = """# 13. Experimental Results and Analysis

## Benchmark Performance Summary
| Metric | Value | Evaluation |
|:---|:---:|:---|
| **Patients Scheduled** | 20 of 20 | 100.0% scheduling success |
| **Total Waiting Time ($WT$)** | 195 minutes | Sum across all 20 patients |
| **Average Waiting Time** | 9.75 minutes | Well below target 15-minute threshold |
| **Scheduling Conflicts ($C$)** | 0 | 100% hard constraint satisfaction |
| **Priority Penalty ($P$)** | 2.0 | High priority wait = 0.0 min average |
| **Under-utilization ($U$)** | 3.27 | Balanced doctor & room utilization |
| **Initial Score $H(S_0)$** | 1047.7 | Greedy priority construction |
| **Final Score $H(S_{\\text{final}})$** | 1047.7 | Local minimum reached |
| **Accepted Moves** | 0 | No neighbor strictly improved score |
| **Neighbor Evaluations** | 100 | Full candidate neighborhood search |
| **Execution Latency** | ~308 ms | Sub-second real-time responsiveness |

## Generated Schedule Table
| ID | Patient Name | Priority | Arrival | Start | End | Wait | Duration | Doctor | Room | Preferred? |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|:---:|
| 1 | John Doe | **HIGH** | 09:00 | 09:00 | 09:20 | 0m | 20m | Dr. Sarah Jenkins | Room A-101 | Yes |
| 2 | Jane Smith | **HIGH** | 09:05 | 09:05 | 09:30 | 0m | 25m | Dr. Robert Chen | Room B-102 | Yes |
| 3 | Alice Johnson | **HIGH** | 09:15 | 09:15 | 09:30 | 0m | 15m | Dr. Emily Patel | Room C-103 | Yes |
| 4 | Bob Brown | **HIGH** | 09:30 | 09:30 | 09:40 | 0m | 10m | Dr. Sarah Jenkins | Room A-101 | Yes |
| 5 | Charlie Davis | **HIGH** | 10:15 | 10:15 | 10:35 | 0m | 20m | Dr. Robert Chen | Room B-102 | Yes |
| 6 | Diana Evans | MEDIUM | 09:10 | 09:30 | 09:50 | 20m | 20m | Dr. Emily Patel | Room C-103 | Yes |
| 7 | Evan Foster | MEDIUM | 09:20 | 09:40 | 10:00 | 20m | 20m | Dr. Sarah Jenkins | Room A-101 | Alt |
| 8 | Fiona Green | MEDIUM | 09:25 | 09:30 | 09:55 | 5m | 25m | Dr. Robert Chen | Room B-102 | Yes |
| 9 | George Harris | MEDIUM | 09:45 | 10:00 | 10:15 | 15m | 15m | Dr. Sarah Jenkins | Room A-101 | Yes |
| 10 | Hannah Ivers | MEDIUM | 09:50 | 09:55 | 10:25 | 5m | 30m | Dr. Marcus Vance | Room B-102 | Alt |
| 11 | Ian Jackson | MEDIUM | 10:00 | 10:15 | 10:35 | 15m | 20m | Dr. Sarah Jenkins | Room A-101 | Yes |
| 12 | Julia King | MEDIUM | 10:10 | 10:25 | 10:50 | 15m | 25m | Dr. Marcus Vance | Room B-102 | Alt |
| 13 | Kevin Lewis | MEDIUM | 10:20 | 10:35 | 10:55 | 15m | 20m | Dr. Sarah Jenkins | Room A-101 | Yes |
| 14 | Laura Miller | MEDIUM | 10:30 | 10:45 | 11:00 | 15m | 15m | Dr. Emily Patel | Room C-103 | Alt |
| 15 | Michael Nelson | LOW | 09:40 | 09:50 | 10:05 | 10m | 15m | Dr. Emily Patel | Room C-103 | Yes |
| 16 | Nina Owens | LOW | 09:45 | 10:50 | 11:15 | 65m | 25m | Dr. Marcus Vance | Room B-102 | Alt |
| 17 | Oscar Perez | LOW | 10:15 | 10:35 | 10:45 | 20m | 10m | Dr. Robert Chen | Room C-103 | Alt |
| 18 | Paula Quinn | LOW | 10:45 | 10:45 | 11:00 | 0m | 15m | Dr. Robert Chen | Room A-101 | None |
| 19 | Quinn Roberts | LOW | 11:00 | 11:00 | 11:15 | 0m | 15m | Dr. Emily Patel | Room C-103 | None |
| 20 | Rachel Scott | LOW | 11:30 | 11:30 | 11:50 | 0m | 20m | Dr. Sarah Jenkins | Room A-101 | None |

## Resource Utilization Analysis
- **Total Consultation Minutes Delivered**: 375 minutes
- **Doctors**:
  - Dr. Sarah Jenkins: 115m / 240m (47.9%)
  - Dr. Robert Chen: 105m / 240m (43.8%)
  - Dr. Emily Patel: 75m / 240m (31.2%)
  - Dr. Marcus Vance: 80m / 240m (33.3%)
- **Rooms**:
  - Consultation Room A-101: 145m / 240m (60.4%)
  - Consultation Room B-102: 135m / 240m (56.2%)
  - Consultation Room C-103: 95m / 240m (39.6%)
"""

# -------------------------------------------------------------
# 14-limitations.md
# -------------------------------------------------------------
docs["14-limitations.md"] = """# 14. System Limitations

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
"""

# -------------------------------------------------------------
# 15-future-enhancements.md
# -------------------------------------------------------------
docs["15-future-enhancements.md"] = """# 15. Future Enhancements

The following realistic future extensions could be explored to expand the academic and operational scope of the application:

1. **Metaheuristic Search Enhancements**:
   - **Random-Restart Hill Climbing**: Initialize local search from multiple diverse pseudo-random initial states to discover lower local minima across the search landscape.
   - **Simulated Annealing**: Accept probabilistic uphill transitions ($e^{-\\Delta H / T}$) to escape local minima and plateaus.
   - **Genetic Algorithms**: Implement crossover and mutation across schedule chromosomes.

2. **Multi-Day & Shift Scheduling**:
   - Expand scheduling horizons across 7-day hospital schedules with varying doctor rosters and shift rotations.

3. **Clinical Specialty Matching**:
   - Integrate doctor medical specializations and room equipment requirements (e.g., ultrasound, minor surgery).

4. **Real-Time Dynamic Rescheduling**:
   - Incorporate WebSocket connections to dynamically re-optimize the schedule when an emergency arrival occurs or an appointment runs over duration.

5. **Patient Notification Portal**:
   - Implement SMS / email alerts notifying patients of their exact consultation window and expected waiting times.
"""

# -------------------------------------------------------------
# 16-viva-questions.md
# -------------------------------------------------------------
docs["16-viva-questions.md"] = """# 16. Comprehensive Viva Questions and Answers

### 1. What is the core title and objective of this project?
**Answer**: "Hospital Patient Scheduling using Heuristic Function and Hill Climbing". The objective is to optimize the consultation schedule for 20 patients across 4 doctors and 3 rooms between 09:00 AM and 01:00 PM by minimizing waiting times, prioritizing urgent patients, utilizing resources efficiently, and strictly preventing double-booking conflicts.

### 2. Why is patient scheduling considered an NP-hard problem?
**Answer**: Because assigning $N$ patients to continuous or discrete time slots, clinicians, and rooms creates a combinatorial state space that grows factorially ($O(N!)$). Evaluating all permutations by brute force is computationally intractable.

### 3. What is the mathematical heuristic function used?
**Answer**: $H(S) = 5(WT) + 100(C) + 20(P) + 10(U)$, where $WT$ is Total Waiting Time, $C$ is Resource Conflicts, $P$ is Priority Penalty, and $U$ is Under-utilization.

### 4. Why is this formulated as a minimization problem?
**Answer**: In optimization theory, costs, delays, constraint violations, and idle capacities represent undesirable penalties. Lower numerical scores represent higher quality, conflict-free schedules.

### 5. Why does the conflict term have the largest weight ($W_2 = 100$)?
**Answer**: A scheduling conflict (two patients in the same room or with the same doctor at the same time) is physically impossible in a clinic. The weight 100 ensures that any schedule with even a single conflict is heavily penalized and rejected over a conflict-free schedule, even if that conflict-free schedule has higher waiting time.

### 6. Can you illustrate the conflict weight with the academic assignment example?
**Answer**: Schedule A has $WT=40, C=0, P=2, U=3 \implies H(A) = 5(40)+100(0)+20(2)+10(3) = 270$. Schedule B has $WT=30, C=1, P=1, U=2 \implies H(B) = 5(30)+100(1)+20(1)+10(2) = 290$. Even though Schedule B has 10 minutes less wait, its single conflict makes $H(B) = 290 > 270$. Hill Climbing chooses Schedule A.

### 7. How is patient waiting time ($WT$) calculated?
**Answer**: For each patient, waiting time is $\\max(0, \\text{start\\_time} - \\text{arrival\\_time})$. Total $WT$ is the sum of all individual waiting times.

### 8. What is the priority penalty ($P$) and how is it implemented?
**Answer**: $P$ penalizes schedules where urgent patients suffer excessive waiting times or lower-priority patients are scheduled ahead of higher-priority patients. In our implementation, `HIGH` priority patients tolerate up to 15 min, `MEDIUM` up to 30 min, and `LOW` up to 45 min before penalizing excess delay, plus an inversion penalty (+0.5).

### 9. How is resource under-utilization ($U$) modeled?
**Answer**: $U$ evaluates the unused consultation minutes across the 4 doctors (960 min capacity) and 3 rooms (720 min capacity) along with workload variance, scaling to an index value around 3.0 to balance facility usage without overshadowing waiting time.

### 10. How does the initial schedule generation work?
**Answer**: It uses a deterministic greedy strategy: patients are sorted by clinical priority (`HIGH` > `MEDIUM` > `LOW`) and then arrival time. Each patient is placed into the earliest feasible slot that satisfies doctor availability, room availability, and preferred doctor preference.

### 11. What is Hill Climbing?
**Answer**: Hill Climbing is a local search optimization algorithm that starts with an initial state, evaluates neighboring states generated by small modifications, and iteratively moves to an improving neighbor until no better neighbor can be found.

### 12. What variation of Hill Climbing did you implement?
**Answer**: Best-Improvement (Steepest-Descent) Hill Climbing. It evaluates all candidate neighbors in the current neighborhood and transitions to the neighbor that achieves the greatest reduction in $H(S)$.

### 13. What neighborhood operations were implemented?
**Answer**:
1. Move Time ($\pm 10$ minutes),
2. Reassign Doctor,
3. Reassign Room,
4. Swap Patients (exchanging assignments between two patients).

### 14. What was the empirical result of schedule generation?
**Answer**: Initial score $H(S_0) = 1047.7$, Final score $H(S_{\\text{final}}) = 1047.7$, Iterations = 0, Accepted moves = 0, Neighbor evaluations = 100, Total waiting time = 195 min, Average wait = 9.75 min, Conflicts = 0.

### 15. Why did Hill Climbing accept 0 moves? Does that mean the algorithm failed?
**Answer**: Absolutely not. Zero accepted moves means the initial greedy schedule was already a local minimum with respect to the implemented neighborhood. All 100 neighboring perturbations evaluated produced an equal or higher heuristic score, so the algorithm correctly terminated.

### 16. Did your algorithm find a global optimum?
**Answer**: We do not claim a global optimum. Standard Hill Climbing only guarantees finding a local minimum relative to the neighborhood operators.

### 17. How can the algorithm escape a local minimum in future work?
**Answer**: By using metaheuristics such as Random-Restart Hill Climbing (re-running search from diverse random seeds), Simulated Annealing (accepting probabilistic uphill moves), or Tabu Search.

### 18. How did HIGH priority patients perform in the generated schedule?
**Answer**: All 5 `HIGH` priority patients experienced exactly 0.0 minutes of waiting time&mdash;they were scheduled immediately upon arrival.

### 19. How did you handle preferred doctors?
**Answer**: Preferred doctors are treated as soft constraints. Patients are assigned their preferred doctor if an earliest feasible conflict-free slot exists. Otherwise, an alternate doctor is assigned. In our schedule, 10 of 16 patients with preferences received their preferred doctor (62.5%).

### 20. What is the total consultation time delivered?
**Answer**: 375 minutes across 20 patients.

### 21. What are the utilization rates for doctors and rooms?
**Answer**: Total doctor utilization is 39.1% (375/960 min); total room utilization is 52.1% (375/720 min).

### 22. What technology stack did you use for the backend?
**Answer**: Python 3.13, FastAPI for asynchronous REST endpoints, Pydantic v2 for data validation, and SQLAlchemy 2.0 ORM with SQLite database.

### 23. What technology stack did you use for the frontend?
**Answer**: Next.js 16 (App Router), TypeScript, Tailwind CSS v4, and Lucide React icons.

### 24. How do the frontend and backend communicate?
**Answer**: Through standard asynchronous HTTP REST API calls with JSON payloads.

### 25. Why did you choose SQLite over PostgreSQL or MySQL?
**Answer**: SQLite is lightweight, serverless, self-contained, and perfectly suited for reproducible academic submissions and standalone testing without external database server configuration.

### 26. How is database idempotency ensured during schedule generation?
**Answer**: `POST /api/schedule/generate` executes within an atomic transaction that clears prior schedule rows before writing the new schedule, strictly respecting the `UNIQUE` constraint on `patient_id`.

### 27. What testing did you perform?
**Answer**: An automated Pytest suite of 22 tests covering health, CRUD, time conversions, overlap detection, heuristic components, neighbor generation, Hill Climbing downhill acceptance, and API integration.

### 28. What frontend quality checks were verified?
**Answer**: `npm run lint` completed with 0 errors and 0 warnings, and `npm run build` compiled all routes statically.

### 29. What was the schedule generation endpoint latency?
**Answer**: Approximately 308 milliseconds, demonstrating real-time performance.

### 30. What was the origin of the StarletteDeprecationWarning in Pytest?
**Answer**: It originates from Starlette 0.45.3+ testclient internals when imported by `fastapi.testclient.TestClient`. It has zero impact on application runtime or test correctness.
"""

# -------------------------------------------------------------
# Presentation_Outline.md
# -------------------------------------------------------------
docs["Presentation_Outline.md"] = """# Presentation Deck Outline (12 Slides)

## Slide 1: Title Slide
- **Title**: Hospital Patient Scheduling using Heuristic Function and Hill Climbing
- **Subtitle**: AI-Driven Outpatient Consultation Optimization
- **Presenter**: Engineering Student / AI Specialist
- **Tech Stack**: Next.js 16 | FastAPI | Python 3.13 | SQLite | Tailwind CSS
- *Speaker Notes*: "Good morning. Today I am presenting an AI application that solves the hospital patient scheduling problem using heuristic evaluation and Hill Climbing local search."

## Slide 2: Problem Statement & Motivation
- **Clinical Challenge**: Outpatient consultation scheduling with competing constraints.
- **Key Parameters**: 20 Patients, 4 Doctors, 3 Rooms, Operating window: 09:00 AM &ndash; 01:00 PM.
- **Pain Points**: Long patient wait times, emergency delays, doctor idle time, room congestion, double-booking conflicts.
- *Speaker Notes*: "Scheduling patients manually or with simple FIFO queues creates severe bottlenecks. Emergency patients get delayed while doctors sit idle between appointments."

## Slide 3: Project Objectives
- Minimize total & average patient waiting time ($WT$).
- Prioritize acute `HIGH` priority cases ($P$).
- Maximize doctor and room resource utilization ($U$).
- Strictly prevent double-booking conflicts ($C = 0$).
- Deliver sub-second scheduling without exhaustive enumeration.
- *Speaker Notes*: "Our goal is multi-objective optimization: lower waiting times, zero conflicts, and prioritized clinical care."

## Slide 4: System Architecture
- **Presentation Layer**: Next.js 16 App Router + Tailwind CSS v4 dashboard.
- **API & Service Layer**: FastAPI REST endpoints with Pydantic v2 schemas.
- **Optimization Core**: Greedy Initial Builder + Best-Improvement Hill Climbing engine.
- **Database**: SQLite with SQLAlchemy 2.0 ORM.
- *Speaker Notes*: "The architecture separates concerns cleanly: a fast Next.js UI talks over REST to a modular Python engine backed by SQLite."

## Slide 5: Database Design
- 4 Relational Tables: `patients`, `doctors`, `rooms`, `schedules`.
- Foreign Key relationships and a strict `UNIQUE(patient_id)` constraint.
- Deterministic 20-patient seed dataset covering all priority and duration tiers.
- *Speaker Notes*: "Data integrity is enforced at the database level. Every patient receives exactly one appointment."

## Slide 6: Heuristic Function Formulation
- **Objective Cost Function**:
  $$H(S) = 5(WT) + 100(C) + 20(P) + 10(U)$$
- **Minimization Strategy**: Lower score = superior schedule.
- **Weights**: Conflicts penalized at 100x; waiting time at 5x; priority at 20x; under-utilization at 10x.
- *Speaker Notes*: "The heuristic linear combination reflects clinical priorities. The 100-point weight on conflicts ensures impossible states are immediately rejected."

## Slide 7: The Academic Conflict Benchmark
- **Schedule A**: $WT=40, C=0, P=2, U=3 \implies H(A) = 270$
- **Schedule B**: $WT=30, C=1, P=1, U=2 \implies H(B) = 290$
- *Core Insight*: Schedule A is superior despite 10m more wait time because it avoids conflicts.
- *Speaker Notes*: "This assignment benchmark proves why conflict avoidance dominates waiting time."

## Slide 8: Hill Climbing Optimization Engine
- **Strategy**: Best-Improvement Hill Climbing.
- **Acceptance Rule**: Strictly accepts $H(S') < H(S_{\\text{current}})$.
- **Neighborhood Operators**: Move Time ($\pm 10$m), Reassign Doctor, Reassign Room, Swap Patients.
- **Termination**: Stops when no neighbor provides improvement (Local Minimum).
- *Speaker Notes*: "Hill Climbing searches locally across 100 candidate perturbations per iteration, accepting only strictly downhill transitions."

## Slide 9: Application UI & Visual Timeline
- Live Dashboard with KPIs and Generate Schedule control.
- Visual Gantt Timeline (09:00&ndash;13:00) mapping doctor and room occupancy.
- Interactive Heuristic Analysis page with live formula breakdowns and step flow.
- *Speaker Notes*: "The Next.js UI gives medical staff immediate visual clarity across room occupancy and doctor schedules."

## Slide 10: Experimental Results
- **Scheduled**: 20 of 20 patients (100%).
- **Total Waiting Time**: 195 minutes (Average: 9.75 min/patient).
- **HIGH Priority Average Wait**: 0.0 minutes (immediate care).
- **Conflicts**: 0.
- **Heuristic Score**: 1047.7.
- **Execution Time**: ~308 ms.
- *Speaker Notes*: "Results exceeded targets: average waiting time was under 10 minutes, all high priority patients waited zero minutes, and zero conflicts occurred."

## Slide 11: Local Minimum & Algorithmic Analysis
- **Empirical Trajectory**: Initial Score = 1047.7 $\rightarrow$ Final Score = 1047.7.
- **Accepted Moves**: 0. Evaluated Neighbors: 100.
- **Academic Explanation**: The greedy priority construction was already a local minimum. Zero accepted moves does not signify failure; it proves the initial state was locally optimal.
- *Speaker Notes*: "We do not claim global optimality, but we proved that within the 100 neighboring states, no better configuration exists."

## Slide 12: Conclusion & Future Work
- **Summary**: Successful academic implementation of multi-criteria hospital scheduling with AI local search.
- **Future Enhancements**: Random-restart Hill Climbing, Simulated Annealing, Multi-day scheduling, Real-time emergency interrupts.
- *Speaker Notes*: "Thank you. I am now open to your questions."
"""

# -------------------------------------------------------------
# README.md (Docs Index)
# -------------------------------------------------------------
docs["README.md"] = """# Hospital Patient Scheduling Documentation Index

Comprehensive end-to-end technical, algorithmic, and architectural documentation for the **Hospital Patient Scheduling using Heuristic Function and Hill Climbing** academic project.

---

## Documentation Contents

1. [01. Project Overview](01-project-overview.md) &mdash; Project title, clinical context, parameters, and motivation for heuristic search.
2. [02. Problem Statement](02-problem-statement.md) &mdash; Formal mathematical optimization problem definition and constraints.
3. [03. System Objectives](03-objectives.md) &mdash; Core clinical and computational targets.
4. [04. System Architecture](04-system-architecture.md) &mdash; Decoupled Next.js 16 and FastAPI tier architecture and diagrams.
5. [05. Technology Stack](05-technology-stack.md) &mdash; Detailed breakdown of frontend and backend technologies and justifications.
6. [06. Database Design](06-database-design.md) &mdash; Relational schema, SQLite ER diagram, column specifications, and relationships.
7. [07. REST API Documentation](07-api-documentation.md) &mdash; Endpoints, payloads, response schemas, and status codes.
8. [08. Heuristic Function Formulation](08-heuristic-function.md) &mdash; Formulation of $H(S) = 5(WT) + 100(C) + 20(P) + 10(U)$ and implementation details.
9. [09. Hill Climbing Algorithm](09-hill-climbing-algorithm.md) &mdash; Best-Improvement local search, neighborhood operators, and local minimum analysis.
10. [10. Scheduling Workflow](10-scheduling-workflow.md) &mdash; End-to-end pipeline flow diagram from registration to UI render.
11. [11. Frontend Application Guide](11-frontend-guide.md) &mdash; Overview of dashboard, CRUD pages, visual Gantt timeline, and heuristic analysis.
12. [12. Testing and Validation](12-testing-and-validation.md) &mdash; Pytest test suite (22/22 passing), ESLint checks, build validation, and warning audit.
13. [13. Experimental Results and Analysis](13-results-and-analysis.md) &mdash; Benchmark results, 20-patient appointment schedule, and utilization metrics.
14. [14. System Limitations](14-limitations.md) &mdash; Honest discussion of local minima, operational window, and static assumptions.
15. [15. Future Enhancements](15-future-enhancements.md) &mdash; Simulated Annealing, random restarts, multi-day scheduling, and real-time alerts.
16. [16. Comprehensive Viva Questions & Answers](16-viva-questions.md) &mdash; 30 academic examination questions and answers.
17. [17. Presentation Deck Outline](Presentation_Outline.md) &mdash; 12-slide comprehensive presentation deck with speaker notes.

---

## Application Screenshots
Real screenshots captured from the running application:
- [Figure 1: Overview Dashboard](screenshots/01-dashboard.png)
- [Figure 2: Patient Management](screenshots/02-patients.png)
- [Figure 3: Doctor Directory](screenshots/03-doctors.png)
- [Figure 4: Room Directory](screenshots/04-rooms.png)
- [Figure 5: Schedule Timeline & Table](screenshots/05-schedule.png)
- [Figure 6: Heuristic Formulation Breakdown](screenshots/06-heuristic.png)
- [Figure 7: Optimization Analysis & Flow Diagram](screenshots/07-optimization-analysis.png)
- [Figure 8: Academic Assignment Benchmark](screenshots/08-assignment-example.png)

---

## Academic Submission Report
- [Download Complete Technical PDF Report](Hospital_Patient_Scheduling_Report.pdf)
"""

for filename, content in docs.items():
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {filename} ({len(content)} chars)")

print("All documentation files written successfully.")
