import os
import time

from celery import Celery

celery = Celery(
    __name__,
    broker=f'amqp://{os.environ.get("RABBITMQ_HOST")}:{os.environ.get("RABBITMQ_PORT_AMQP")}',
    backend=f'redis://{os.environ.get("REDIS_HOSTNAME")}:{os.environ.get("REDIS_PORT")}/0',
)


def celery_task_sender(task: Celery.Task):
    def wrapper(*args, **kwargs):
        return task.delay(*args, **kwargs)

    return wrapper


@celery_task_sender
@celery.task(name="send_email")
def send_email(email, message):
    time.sleep(5)  # Simulate creation and sending of email
    return f"Email sent to {email}: {message}"
