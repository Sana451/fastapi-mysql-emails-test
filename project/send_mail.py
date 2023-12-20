import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

load_dotenv()
MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_PORT=2525,
    MAIL_SERVER="smtp.mail.ru",
    MAIL_FROM_NAME="Sana",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
