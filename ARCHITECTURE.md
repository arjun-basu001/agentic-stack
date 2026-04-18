# Architecture: Enterprise Agentic E-Commerce

## 1. Goals

This repository acts as a practical reference implementation for:

1. Production-oriented e-commerce backend design
2. Agentic AI harness patterns (portable brain + multi-agent + tools + memory)
3. Clear separation between framework and harness concerns

## 2. Layered Application Design

- **API layer (`app/api`)**: FastAPI routes and dependency wiring
- **Application/service layer (`app/services`)**: e-commerce business logic
- **Domain model layer (`app/models`)**: core entities and relationships
- **Infrastructure (`app/db`, `app/core`)**: persistence, logging, config, auth
- **Agent harness (`app/agents`)**: long-running memory + tools + orchestration

This follows domain-driven boundaries and keeps business logic outside route handlers.

## 3. Portable Brain Pattern

The `.agent/` directory is the harness-agnostic brain:

- `working/`: transient session artifacts and intermediate plans
- `episodic/`: append-only event journals (`events.jsonl`)
- `semantic/`: promoted lessons and generalized patterns (`lessons.jsonl`)
- `personal/`: user/team preferences (`preferences.json`)

`PortableBrain` provides APIs to read/write these layers and supports a compounding learning workflow.

## 4. Multi-Agent System

- **RecommendationAgent**: user-targeted product recommendations
- **CustomerServiceAgent**: support response routing/intents
- **InventoryAgent**: stock check and reorder triggers

`AgentOrchestrator` composes these agents and injects tool access via `ToolRegistry`.

## 5. Tool Integration Pattern

`ToolRegistry` abstracts external/internal capabilities as typed tools:

- `recommend_products`
- `get_inventory`

This makes capabilities discoverable, composable, and testable.

## 6. State and Memory

- **Transactional state**: SQLAlchemy + relational DB (orders, inventory, carts)
- **Session/runtime state**: `.agent/working`
- **Behavioral memory**: `.agent/episodic` logs
- **Graduated memory**: `.agent/semantic` lessons
- **Preference memory**: `.agent/personal`

## 7. Observability

- Request-level logging middleware with method/path/status/duration
- Agent event logging through `BaseAgent.observe`
- Journaling agent events into `.agent/episodic/events.jsonl`

## 8. Production Hardening Roadmap

- Move SQLite to managed Postgres
- Add migrations (Alembic)
- Add queue workers for asynchronous order workflows
- Add RBAC and scoped authZ policies
- Add OpenTelemetry traces + metrics export
- Add CI/CD gates with unit/integration/contract tests
