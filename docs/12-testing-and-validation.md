# 12. Testing and Validation

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
rootdir: C:\Users\HP\Desktop\AI_project\backend
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
