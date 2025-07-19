from celery import Celery

celery_app = Celery(
    "telegram_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
    include=["bot.tasks"]
)

celery_app.conf.timezone = 'UTC'
