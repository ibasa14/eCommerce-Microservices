import os
import time

from celery import Celery

celery = Celery(
    __name__,
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND"),
)


def celery_task_sender(task: Celery.Task):
    def wrapper(*args, **kwargs):
        return task.delay(*args, **kwargs)

    return wrapper


@celery_task_sender
@celery.task(name="send_email")
def send_email(email, message):
    time.sleep(5)
    return f"Email sent to {email}: {message}"
