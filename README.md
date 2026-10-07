mail_service/
│
├── config/
│   ├── __init__.py
│   └── settings.py       # Pydantic BaseSettings (валидация env)
│
├── tasks/
│   ├── __init__.py
│   ├── worker.py         # Инициализация Celery
│   └── mail_tasks.py     # Сами таски для отправки писем
│
├── schemas/
│   ├── __init__.py
│   └── mail.py           # Pydantic-схемы для валидации API
│
├── templates/
│   └── welcome.html      # Jinja2 шаблон письма
│
├── api/
│   ├── __init__.py
│   └── endpoints.py      # Роуты FastAPI
│
├── main.py               # Точка входа ASGI
└── Dockerfile
