from kafka import KafkaConsumer
import psycopg2
import json
from config import Config

# Kafka consumer configuration
KAFKA_TOPIC = "your_topic"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="your_group_id",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

# PostgreSQL connection configuration
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "your_database"
POSTGRES_USER = "your_user"
POSTGRES_PASSWORD = "your_password"

conn = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    log_data JSONB
)
""")
conn.commit()

# Consume messages from Kafka and save to PostgreSQL
for message in consumer:
    log_data = message.value
    cursor.execute(
        "INSERT INTO logs (log_data) VALUES (%s)", [json.dumps(log_data)]
    )
    conn.commit()

# Close the connection
cursor.close()
conn.close()
