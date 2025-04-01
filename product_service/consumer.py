import pika

params = pika.URLParameters('amqps://cbrquzeq:bSGQZrdqhii4NQmaaqO6azfDbVR7VES8@shrimp.rmq.cloudamqp.com/cbrquzeq')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='config')


def callback(ch, method, properties, body):
    print('received config')
    print(body)


channel.basic_consume(queue='config', on_message_callback=callback, auto_ack=True)

print('start consuming')

channel.start_consuming()


channel.close()


