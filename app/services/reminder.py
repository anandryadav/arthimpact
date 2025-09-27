from __future__ import annotations

from datetime import date, timedelta
from typing import List

from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import SessionLocal
from ..models.entities import ServiceContract
from ..utils.flags import expiry_flag, payment_flag
from .emailer import send_email_sync


def build_reminder_email(services: List[ServiceContract]) -> str:
    lines = [
        "Daily Service Reminder:",
        "",
    ]
    for s in services:
        lines.append(
            f"Vendor #{s.vendor_id} | {s.service_name} | Expiry: {s.expiry_date} | Payment Due: {s.payment_due_date}"
        )
    return "\n".join(lines)


def run_daily_reminder_job() -> int:
    db: Session = SessionLocal()
    try:
        today = date.today()
        cutoff = today + timedelta(days=settings.REMINDER_DAYS)
        candidates = (
            db.query(ServiceContract)
            .filter((ServiceContract.expiry_date <= cutoff) | (ServiceContract.payment_due_date <= cutoff))
            .all()
        )
        flagged = [s for s in candidates if expiry_flag(s.expiry_date) or payment_flag(s.payment_due_date)]

        if flagged and settings.SMTP_FROM and settings.SMTP_HOST:
            body = build_reminder_email(flagged)
            send_email_sync("Service Reminders", [settings.SMTP_FROM], body)
        return len(flagged)
    finally:
        db.close()


