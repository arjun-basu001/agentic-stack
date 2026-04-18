import json
import logging
import time
from pathlib import Path

from fastapi import FastAPI, Request

from app.api.routes import agents, auth, carts, inventory, orders, products, search
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.init_db import seed_data
from app.db.session import SessionLocal, engine
from app.models.user import Base

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)


@app.middleware("http")
async def request_observability(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    logger.info(
        "http_request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration, 2),
        },
    )
    return response


@app.on_event("startup")
def on_startup() -> None:
    Path("data").mkdir(exist_ok=True)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

    # Ensure portable brain scaffold exists
    for p in [".agent/working", ".agent/episodic", ".agent/semantic", ".agent/personal"]:
        Path(p).mkdir(parents=True, exist_ok=True)

    lessons = Path(".agent/semantic/lessons.jsonl")
    if not lessons.exists():
        lessons.write_text(
            json.dumps({"topic": "checkout", "lesson": "Always validate inventory before order placement."}) + "\n",
            encoding="utf-8",
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(products.router, prefix=settings.api_prefix)
app.include_router(carts.router, prefix=settings.api_prefix)
app.include_router(orders.router, prefix=settings.api_prefix)
app.include_router(inventory.router, prefix=settings.api_prefix)
app.include_router(search.router, prefix=settings.api_prefix)
app.include_router(agents.router, prefix=settings.api_prefix)
