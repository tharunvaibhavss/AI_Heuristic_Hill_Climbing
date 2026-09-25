# 13. Experimental Results and Analysis

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
| **Final Score $H(S_{\text{final}})$** | 1047.7 | Local minimum reached |
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
