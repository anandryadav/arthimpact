from __future__ import annotations

from datetime import date

from app.core.config import settings


def days_until(target: date) -> int:
    return (target - date.today()).days


def expiry_flag(expiry_date: date) -> str | None:
    days = days_until(expiry_date)
    if days < 0:
        return "red"
    if days <= settings.REMINDER_DAYS:
        return "yellow"
    return None


def payment_flag(due_date: date) -> str | None:
    days = days_until(due_date)
    if days < 0:
        return "red"
    if days <= settings.REMINDER_DAYS:
        return "yellow"
    return None


