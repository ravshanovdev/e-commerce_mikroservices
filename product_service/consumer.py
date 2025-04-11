import pika
import json

RABBITMQ_URL = 'amqps://cbrquzeq:hKpzYfVT1vv6g-ltdI13it6qfSfUtAoX@shrimp.rmq.cloudamqp.com/cbrquzeq'


def callback(ch, method, properties, body):
    """RabbitMQ dan kelgan login token xabarlarini qayta ishlash"""
    message = json.loads(body)
    username = message["username"]
    token = message["token"]

    print(f"Login qilgan foydalanuvchi: {username}, Token: {token}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    """RabbitMQ tinglovchi (Consumer)"""
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='user_login', durable=True)
    channel.basic_consume(queue='user_login', on_message_callback=callback, auto_ack=True)

    print("Login uchun tokenlar tinglanmoqda...")
    channel.start_consuming()
