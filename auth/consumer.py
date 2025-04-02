import os
import django

# Django sozlamalarini yuklash
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "config.settings")  # "your_project" ni loyihangiz nomiga almashtiring
django.setup()

import json
import pika

from accounts.models import Product, Category

params = pika.URLParameters('amqps://cbrquzeq:bSGQZrdqhii4NQmaaqO6azfDbVR7VES8@shrimp.rmq.cloudamqp.com/cbrquzeq')

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='config')


def callback(ch, method, properties, body):
    print('received config')

    data = json.loads(body)  # json.load() emas, json.loads() ishlatish kerak

    print(data)

    if properties.content_type == 'product_created':
        category, _ = Category.objects.get_or_create(id=data['category'])
        product = Product.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            category_id=category  # `category` emas, `category_id` ishlatish kerak
        )
        product.save()
        print('Product created')

    elif properties.content_type == "created_category":
        category = Category.objects.create(
            name=data['name']
        )
        category.save()
        print('Category created')


channel.basic_consume(queue='config', on_message_callback=callback, auto_ack=True)

print('start consuming')

channel.start_consuming()

channel.close()
