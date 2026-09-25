# 4. System Architecture

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
