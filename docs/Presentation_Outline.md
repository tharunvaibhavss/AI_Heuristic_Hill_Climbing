# Presentation Deck Outline (12 Slides)

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
- **Acceptance Rule**: Strictly accepts $H(S') < H(S_{\text{current}})$.
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
- **Empirical Trajectory**: Initial Score = 1047.7 $ightarrow$ Final Score = 1047.7.
- **Accepted Moves**: 0. Evaluated Neighbors: 100.
- **Academic Explanation**: The greedy priority construction was already a local minimum. Zero accepted moves does not signify failure; it proves the initial state was locally optimal.
- *Speaker Notes*: "We do not claim global optimality, but we proved that within the 100 neighboring states, no better configuration exists."

## Slide 12: Conclusion & Future Work
- **Summary**: Successful academic implementation of multi-criteria hospital scheduling with AI local search.
- **Future Enhancements**: Random-restart Hill Climbing, Simulated Annealing, Multi-day scheduling, Real-time emergency interrupts.
- *Speaker Notes*: "Thank you. I am now open to your questions."
