
import pika
import json

RABBITMQ_URL = 'amqps://cbrquzeq:hKpzYfVT1vv6g-ltdI13it6qfSfUtAoX@shrimp.rmq.cloudamqp.com/cbrquzeq'


def send_user_created_event(user_data):
    """Foydalanuvchi yaratilganda xabar yuborish"""
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="user_created", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="user_created",
        body=json.dumps(user_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Xabarni saqlash uchun
        ),
    )

    print("User yaratildi va RabbitMQ'ga jo‘natildi!")
    connection.close()


def send_token_event(token_data):
    """Login qilganda tokenni RabbitMQ'ga yuborish"""
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue="user_login", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="user_login",
        body=json.dumps(token_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Xabarni saqlash uchun
        ),
    )

    print("Login uchun token RabbitMQ'ga yuborildi!")
    connection.close()











