from kafka import KafkaProducer
import json
import time
from config import Config

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

try:
    while True:
        # Create a message
        message = {"key": "value", "timestamp": time.time()}

        # Send the message to the Kafka topic
        producer.send(Config.KAFKA_TOPIC, value=message)

        # Print the message for debugging purposes
        print(f"Sent: {message}")

        # Wait for a second before sending the next message
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping the producer...")

# Ensure all messages are sent
producer.flush()

# Close the producer
producer.close()
