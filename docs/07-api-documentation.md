# 7. REST API Documentation

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
