# 5. Technology Stack

The technology stack was selected to provide academic rigor, robust type safety, determinism, and rapid execution.

## Frontend Technologies
| Component | Technology | Version | Rationale |
|:---|:---|:---|:---|
| **Framework** | Next.js (App Router) | 16.3.6 | Modern React framework with static prerendering, zero layout shift, and server component optimization. |
| **Language** | TypeScript | 5.x | Strict end-to-end type safety eliminating runtime null pointer exceptions. |
| **Styling** | Tailwind CSS | v4.0.0 | High-performance atomic utility styling with modern CSS variables. |
| **Icons** | Lucide React | 1.16.0 | Clean, accessible vector icons for medical and algorithmic dashboards. |
| **Bundler** | Turbopack | Built-in | Fast local compilation and sub-second hot reload cycles. |

## Backend Technologies
| Component | Technology | Version | Rationale |
|:---|:---|:---|:---|
| **Runtime** | Python | 3.13.2 | High expressiveness for AI heuristics, algorithmic operations, and data transformations. |
| **Web Framework**| FastAPI | 0.115.x | Asynchronous REST framework with automatic OpenAPI documentation and high throughput. |
| **Validation** | Pydantic | v2.10.x | Strict data validation, regex time format checks, and JSON serialization. |
| **ORM** | SQLAlchemy | 2.0.x | Industrial-strength ORM for relational queries, relationships, and transactional commits. |
| **Database** | SQLite 3 | Embedded | Self-contained, zero-configuration relational database engine ideal for academic reproducibility. |
| **Test Engine** | Pytest & TestClient | 9.1.x | Comprehensive unit and integration test suite with high-speed automated assertions. |
