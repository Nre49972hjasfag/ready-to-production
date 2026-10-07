import asyncio
from pathlib import Path
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from config.settings import settings
from .worker import celery_app

# Настройки соединения  fastapi-mail
mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates'
)

@celery_app.task(
    bind=True, 
    max_retries=3, 
    default_retry_delay=60,  # Повтор через 60 сек если ошибке
    name="tasks.send_templated_email"
)
def send_templated_email(self, recipient: str, subject: str, template_name: str, context: dict):
    """
    Celery task для отправки email. 
    Поскольку fastapi-mail асинхронный, запускаем его в event loop внутри воркера.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        template_body=context,
        subtype=MessageType.html
    )
    
    fm = FastMail(mail_config)
    
    try:
        # Запускаем асинхронную отправку в синхронном контексте Celery
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fm.send_message(message, template_name=template_name))
    except Exception as exc:
        # Экспоненциальный бэк-офф или обычный перезапуск таски при ошибке SMTP
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 30)
