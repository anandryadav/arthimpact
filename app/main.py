from __future__ import annotations

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .core.config import settings
from .core.database import Base, engine, get_db
from .api.v1.routers import auth as auth_router
from .api.v1.routers import vendors as vendors_router
from .api.v1.routers import services as services_router
from .api.v1.routers import reminders as reminders_router
from .services.reminder import run_daily_reminder_job
from apscheduler.schedulers.background import BackgroundScheduler


# Create tables
Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Vendor Management API",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        description="Vendor and Service contract management with reminders (API v1)",
        contact={
            "name": "Support",
            "email": settings.SMTP_FROM or "support@example.com",
        },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routers directly in main app with /api/v1 prefix
    app.include_router(auth_router.router, prefix="/api/v1")
    app.include_router(vendors_router.router, prefix="/api/v1")
    app.include_router(services_router.router, prefix="/api/v1")
    app.include_router(reminders_router.router, prefix="/api/v1")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    # Optional daily scheduler
    if settings.ENABLE_SCHEDULER:
        scheduler = BackgroundScheduler()
        scheduler.add_job(run_daily_reminder_job, "cron", hour=8, minute=0)
        scheduler.start()

    return app


app = create_app()


