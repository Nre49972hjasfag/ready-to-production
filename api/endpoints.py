from fastapi import APIRouter, status
from schemas.mail import EmailSchema
from tasks.mail_tasks import send_templated_email

router = APIRouter(prefix="/v1/notifications", tags=["Notifications"])

@router.post(
    "/welcome-email", 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger welcome email background task"
)
async def trigger_welcome_email(payload: EmailSchema):
    # Отправляем задачу в очередь Redis. Блокировки API не происходит.
    task = send_templated_email.delay(
        recipient=payload.email,
        subject="Добро пожаловать в наш сервис!",
        template_name="welcome.html",
        context={"user_name": payload.user_name}
    )
    
    return {
        "status": "sent_to_queue",
        "task_id": task.id
    }
