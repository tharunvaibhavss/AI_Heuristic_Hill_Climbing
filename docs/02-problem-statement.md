# 2. Problem Statement

## Formal Problem Definition
The objective of the hospital patient scheduling problem is to construct a consultation schedule $S$ that assigns each patient $i \in \{1, \dots, N\}$:
- a consultation start time $t_{\text{start}}(i)$ and end time $t_{\text{end}}(i) = t_{\text{start}}(i) + d_i$,
- an assigned doctor $D(i)$,
- and an assigned examination room $R(i)$,

such that:
1. **Patient Waiting Time ($WT$) is minimized**: The delay between patient arrival time $a_i$ and consultation commencement $t_{\text{start}}(i)$ must be kept as short as possible.
2. **Emergency and High-Priority Patients are expedited**: Patients designated with `HIGH` priority must receive prompt attention without unnecessary delays.
3. **Doctors are utilized efficiently**: Doctor workload should be distributed equitably across the session without long idle periods.
4. **Consultation rooms are utilized efficiently**: Facility turnover should be maintained without bottlenecks.
5. **Hard Scheduling Conflicts ($C$) are eliminated**: Under no circumstances may two patients overlap with the same doctor or within the same consultation room simultaneously.
6. **Doctor Preferences are honored when feasible**: Patient doctor preferences should be respected when open slots permit without inducing conflicts.

## Mathematical Formulation
The optimization problem is formalized as finding an assignment $S^*$:

$$\min_{S \in \mathcal{S}} H(S)$$

subject to hard operational constraints:
- $t_{\text{start}}(i) \ge a_i \quad \forall i$
- $t_{\text{start}}(i) \ge \text{start}(D(i))$ and $t_{\text{end}}(i) \le \text{end}(D(i)) \quad \forall i$
- $t_{\text{start}}(i) \ge \text{start}(R(i))$ and $t_{\text{end}}(i) \le \text{end}(R(i)) \quad \forall i$
- $\text{No doctor overlap}: [t_{\text{start}}(i), t_{\text{end}}(i)) \cap [t_{\text{start}}(j), t_{\text{end}}(j)) = \emptyset \quad \text{if } D(i) = D(j)$
- $\text{No room overlap}: [t_{\text{start}}(i), t_{\text{end}}(i)) \cap [t_{\text{start}}(j), t_{\text{end}}(j)) = \emptyset \quad \text{if } R(i) = R(j)$
