# 11. Frontend Application Guide

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
