# Hospital Patient Scheduling Documentation Index

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
