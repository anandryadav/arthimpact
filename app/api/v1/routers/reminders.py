from __future__ import annotations

from fastapi import APIRouter, Depends

from app.services.deps import get_current_user
from app.services.reminder import run_daily_reminder_job


router = APIRouter(prefix="/reminders", tags=["reminders"]) 


@router.post("/run")
def run_reminders(user=Depends(get_current_user)):
    count = run_daily_reminder_job()
    return {"flagged": count}


