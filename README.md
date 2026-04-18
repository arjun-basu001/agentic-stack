# Agentic Stack: Enterprise Agentic E-Commerce Reference

An enterprise-grade e-commerce backend reference implementation that demonstrates **Agentic AI harness architecture patterns** with a portable brain design.

## Highlights

- FastAPI + SQLAlchemy + SQLite (dev) backend
- Core e-commerce APIs:
  - Product catalog management
  - Shopping cart and checkout
  - Order processing
  - User authentication (JWT)
  - Inventory management
  - Search and recommendations
- Agentic architecture:
  - Portable brain in `.agent/` (working / episodic / semantic / personal)
  - Multi-agent runtime (recommendation, customer service, inventory)
  - Tool registry and orchestrator patterns
  - Session + persistent memory model
  - Structured observability and event journaling

## Project Structure

```text
app/
  api/routes/           # REST endpoints
  agents/               # agent abstractions, memory, tools, orchestrator
  core/                 # config, security, logging
  db/                   # session + seed setup
  models/               # SQLAlchemy entities
  schemas/              # Pydantic DTOs
  services/             # domain/application service layer
.agent/
  working/              # transient task/session state
  episodic/             # action logs/event journals
  semantic/             # promoted lessons
  personal/             # user preferences
```

## Quickstart

### 1) Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

### 2) Run API

```bash
uvicorn app.main:app --reload
```

- Open docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

### 3) Run tests

```bash
pytest -q
```

## Default Seed User

- Email: `admin@agentic-commerce.local`
- Password: `admin123`

## Important Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/products/`
- `POST /api/v1/cart/items`
- `POST /api/v1/orders/checkout`
- `GET /api/v1/search/products?q=laptop`
- `GET /api/v1/search/recommendations`
- `GET /api/v1/agents/recommend`
- `POST /api/v1/agents/support?message=where+is+my+order`
- `GET /api/v1/agents/inventory/{product_id}`

## Reference Docs

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [AGENT.md](./AGENT.md)
