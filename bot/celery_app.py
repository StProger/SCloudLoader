from celery import Celery

celery_app = Celery(
    "telegram_tasks",
    broker="redis://redis:6379/3",
    backend="redis://redis:6379/4",
    include=["bot.tasks"]
)

celery_app.conf.timezone = 'UTC'

celery_app.conf.update(
    task_acks_late=True,         # подтверждаем задачу только после завершения
    worker_prefetch_multiplier=1,  # по одной задаче на воркер
    task_time_limit=300,         # максимум 5 минут на задачу
    task_soft_time_limit=240,    # мягкий лимит — предупредить
    broker_connection_retry_on_startup=True,
)
