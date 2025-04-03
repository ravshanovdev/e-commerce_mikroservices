# import os
# import django
# from django import db
# # Django sozlamalarini yuklash
# os.environ.setdefault("DJANGO_SETTINGS_MODULE",
#                       "config.settings")  # "your_project" ni loyihangiz nomiga almashtiring
# django.setup()
#
# import json
# import pika
#
# from accounts.models import Product, Category
#
# params = pika.URLParameters('amqps://cbrquzeq:bSGQZrdqhii4NQmaaqO6azfDbVR7VES8@shrimp.rmq.cloudamqp.com/cbrquzeq')
#
# connection = pika.BlockingConnection(params)
# channel = connection.channel()
#
# channel.queue_declare(queue='config')
#
#
# def callback(ch, method, properties, body):
#     print('received config')
#
#     data = json.loads(body)  # json.load() emas, json.loads() ishlatish kerak
#
#     print(data)
#
#     if properties.content_type == 'product_created':
#         category, _ = Category.objects.get_or_create(id=data['category'])
#         product = Product.objects.create(
#             name=data['name'],
#             description=data['description'],
#             price=data['price'],
#             stock=data['stock'],
#             category_id=category
#         )
#
#         print('Product created')
#
#     elif properties.content_type == "created_category":
#         category = Category.objects.create(
#             name=data['name']
#         )
#         category.save_base()
#         print('Category created')
#
#
# channel.basic_consume(queue='config', on_message_callback=callback, auto_ack=True)
#
# print('start consuming')
#
# channel.start_consuming()
#
# channel.close()

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











