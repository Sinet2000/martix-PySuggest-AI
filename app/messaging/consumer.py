from kafka import KafkaConsumer
from app.core.config import settings

def start_consumer():
    consumer = KafkaConsumer(
        "events-topic",
        bootstrap_servers=settings.kafka_broker_url,
        group_id="recommendation-engine",
    )
    for message in consumer:
        print(f"Received message: {message.value}")
