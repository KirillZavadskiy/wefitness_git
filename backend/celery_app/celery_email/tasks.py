import smtplib
from email.message import EmailMessage

from celery import shared_task
from starlette.templating import Jinja2Templates

from backend.celery_app.settings import (
    EMAIL_HOST, EMAIL_PASSWORD, EMAIL_PORT,
    EMAIL_USERNAME, FRONTEND_URL
)


@shared_task
def send_txt(to_email: str, token: str):
    confirmation_url = f"{FRONTEND_URL}?token={token}"
    templates = Jinja2Templates("templates")
    template = templates.get_template(name="confirmation_email.html")
    html_content = template.render(confirmation_url=confirmation_url)

    message = EmailMessage()
    message.add_alternative(html_content, subtype="html")
    message["From"] = EMAIL_USERNAME
    message["To"] = to_email
    message["Subject"] = "Подтверждение регистрации"

    with smtplib.SMTP_SSL(
        host=EMAIL_HOST,
        port=EMAIL_PORT
    ) as smtp:
        smtp.login(
            user=EMAIL_USERNAME,
            password=EMAIL_PASSWORD,
        )
        smtp.send_message(msg=message)


@shared_task
def send_xlxs_progress(email: str, file_name: str):
    message = EmailMessage()
    message["From"] = EMAIL_USERNAME
    message["To"] = email
    message["Subject"] = "WeFitness. Ваш прогресс."
    with open(file_name, "rb") as f:
        file_data = f.read()
    message.add_attachment(
        file_data,
        maintype="application",
        subtype="xlsx",
        filename=file_name
    )
    with smtplib.SMTP_SSL(
        host=EMAIL_HOST,
        port=EMAIL_PORT
    ) as smtp:
        smtp.login(
            user=EMAIL_USERNAME,
            password=EMAIL_PASSWORD,
        )
        smtp.send_message(msg=message)
