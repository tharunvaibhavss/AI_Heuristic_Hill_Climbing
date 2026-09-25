# 6. Database Design

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
| `waiting_time` | INTEGER | No | Non-negative integer | Calculated delay ($t_{\text{start}} - a_i$) |
| `created_at` | DATETIME | Yes | DEFAULT UTC NOW | Schedule generation timestamp |
