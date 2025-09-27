from __future__ import annotations

import asyncio
from email.message import EmailMessage
from typing import Iterable

import aiosmtplib

from ..core.config import settings


async def send_email(subject: str, to_emails: Iterable[str], body: str) -> None:
    if not (settings.SMTP_HOST and settings.SMTP_PORT and settings.SMTP_FROM):
        return

    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )


def send_email_sync(subject: str, to_emails: Iterable[str], body: str) -> None:
    asyncio.run(send_email(subject, to_emails, body))


