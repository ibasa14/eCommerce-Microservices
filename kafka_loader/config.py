import os


class Config:
    KAFKA_TOPIC = os.environ.get("APP_DATABASE_URL")
    KAFKA_BOOTSTRAP_SERVERS = os.environ("APP_DATABASE_URL")
    KAFKA_GROUP_ID = os.environ.get("KAFKA_GROUP_ID")
    KAFKA_BOOTSTRAP_SERVERS = (
        f'{os.environ.get("KAFKA_HOST")}:{os.environ.get("KAFKA_PORT")}'
    )
