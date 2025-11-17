# core/rabbitmq.py
import json
import pika
from django.conf import settings


def publish_event(event_name: str, payload: dict):
    """
    یک پیام ساده به RabbitMQ می‌فرستد.
    """
    url = getattr(settings, "RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    queue = getattr(settings, "RABBITMQ_DEFAULT_QUEUE", "app_events")

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # مطمئن می‌شویم صف وجود دارد
    channel.queue_declare(queue=queue, durable=True)

    body = {
        "event": event_name,
        "payload": payload,
    }

    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=2,  # durable
        ),
    )

    connection.close()
