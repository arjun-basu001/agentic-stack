# AGENT.md - Machine-Readable Development Guide

## Purpose

This repository demonstrates an agentic harness for e-commerce. AI agents should follow this file as execution policy.

## Working Rules

1. Keep route handlers thin; place business logic in `app/services`.
2. Persist operational memory in `.agent/episodic` and generalized memory in `.agent/semantic`.
3. Never bypass inventory validation during checkout.
4. Prefer additive, backward-compatible schema and API changes.
5. Update architecture docs when changing harness behavior.

## Commands

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

### Run
```bash
uvicorn app.main:app --reload
```

### Test
```bash
pytest -q
```

## Agent Memory Policy

- **Write transient notes**: `.agent/working/*.json`
- **Write action journals**: `.agent/episodic/events.jsonl`
- **Promote lessons after review**: `.agent/semantic/lessons.jsonl`
- **Store user-specific settings**: `.agent/personal/preferences.json`

## Guardrails

- All order placement must reserve stock first.
- Any new agent tool must be registered in `ToolRegistry` with clear description.
- Critical behavior changes require updates in `ARCHITECTURE.md` and README.
