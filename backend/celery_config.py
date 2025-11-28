from celery.schedules import crontab

broker_url="redis://localhost:6379/0"
result_backend="redis://localhost:6379/0"
Timezone="Asia/Kolkata"
broker_connection_retry_on_startup=True

beat_schedule = {
    "daily_reminder": {
        "task": "daily_reminder",
        "schedule": crontab(minute="*/2"),
    },
    "monthly_report": {
        "task": "monthly_report",
        "schedule": crontab(minute="*/5"),
    }
}