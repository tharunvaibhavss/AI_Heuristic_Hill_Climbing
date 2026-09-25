# 15. Future Enhancements

The following realistic future extensions could be explored to expand the academic and operational scope of the application:

1. **Metaheuristic Search Enhancements**:
   - **Random-Restart Hill Climbing**: Initialize local search from multiple diverse pseudo-random initial states to discover lower local minima across the search landscape.
   - **Simulated Annealing**: Accept probabilistic uphill transitions ($e^{-\Delta H / T}$) to escape local minima and plateaus.
   - **Genetic Algorithms**: Implement crossover and mutation across schedule chromosomes.

2. **Multi-Day & Shift Scheduling**:
   - Expand scheduling horizons across 7-day hospital schedules with varying doctor rosters and shift rotations.

3. **Clinical Specialty Matching**:
   - Integrate doctor medical specializations and room equipment requirements (e.g., ultrasound, minor surgery).

4. **Real-Time Dynamic Rescheduling**:
   - Incorporate WebSocket connections to dynamically re-optimize the schedule when an emergency arrival occurs or an appointment runs over duration.

5. **Patient Notification Portal**:
   - Implement SMS / email alerts notifying patients of their exact consultation window and expected waiting times.
