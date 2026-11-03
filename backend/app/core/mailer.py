"""Adaptador SMTP (TRD §3.1: adapters). Nunca registra el contenido del mensaje."""
import logging
import smtplib
from email.message import EmailMessage

from app.core.config import get_settings

logger = logging.getLogger("rutalibre.mail")


def send_email(to: str, subject: str, body: str) -> None:
    s = get_settings()
    msg = EmailMessage()
    msg["From"] = s.mail_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=10) as smtp:
            if s.smtp_starttls:
                smtp.starttls()
            if s.smtp_user:
                smtp.login(s.smtp_user, s.smtp_password)
            smtp.send_message(msg)
    except Exception:
        # Se loguea solo el hecho; el cuerpo contiene el token de recuperación.
        logger.error("No se pudo enviar el email de recuperación (SMTP %s:%s).", s.smtp_host, s.smtp_port)
