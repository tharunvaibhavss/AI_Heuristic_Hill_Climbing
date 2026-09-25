# 8. Heuristic Function Formulation

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
For each scheduled patient $i \in \{1, \dots, N\}$, waiting time is defined as the elapsed duration between patient arrival time $a_i$ and scheduled consultation commencement $t_{\text{start}}(i)$:

$$WT = \sum_{i=1}^{N} \max(0, t_{\text{start}}(i) - a_i)$$

In the benchmark schedule:
$$WT = 195 \text{ minutes} \implies 5 \times 195 = 975.0$$

## Term 2: Scheduling Conflicts ($C$)
$C$ represents the count of overlapping interval pairs:
- **Doctor Overlap**: Patient $i$ and $j$ assigned to the same doctor where $[t_{\text{start}}(i), t_{\text{end}}(i)) \cap [t_{\text{start}}(j), t_{\text{end}}(j)) \ne \emptyset$.
- **Room Overlap**: Patient $i$ and $j$ assigned to the same room where $[t_{\text{start}}(i), t_{\text{end}}(i)) \cap [t_{\text{start}}(j), t_{\text{end}}(j)) \ne \emptyset$.

In the benchmark schedule:
$$C = 0 \implies 100 \times 0 = 0.0$$

## Term 3: Priority Penalty ($P$)
The academic assignment specifies that emergency and high-priority patients must be prioritized, but leaves the exact implementation to the engineer. The implemented formula in `backend/app/services/scheduling/heuristic.py` evaluates:
1. **Excess Delay Thresholds**:
   - `HIGH` priority tolerates up to 15 min wait: $\text{penalty} += \lceil \max(0, \text{wait} - 15) / 5 \rceil$.
   - `MEDIUM` priority tolerates up to 30 min wait: $\text{penalty} += \lceil \max(0, \text{wait} - 30) / 10 \rceil$.
   - `LOW` priority tolerates up to 45 min wait: $\text{penalty} += \lceil \max(0, \text{wait} - 45) / 15 \rceil$.
2. **Priority Ordering Inversion**:
   - Assesses a $+0.5$ penalty if a lower-priority patient begins consultation earlier than an already-waiting higher-priority patient.

In the benchmark schedule:
$$P = 2.0 \implies 20 \times 2.0 = 40.0$$

## Term 4: Under-Utilization Penalty ($U$)
Defined based on total idle capacity across doctor shifts and room operating hours:
- Doctor Capacity: $4 \times 240 = 960$ minutes. Consultations used: $375$ min (Unused: $585$ min / 60.9%).
- Room Capacity: $3 \times 240 = 720$ minutes. Consultations used: $375$ min (Unused: $345$ min / 47.9%).
- Unused capacity fractions are normalized with a doctor workload standard deviation term, scaling to an index value:
$$U = 3.27 \implies 10 \times 3.27 = 32.7$$

## Total Heuristic Value
$$H(S) = 975.0 + 0.0 + 40.0 + 32.7 = 1047.7$$
