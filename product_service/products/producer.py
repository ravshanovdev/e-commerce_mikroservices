# import pika, json
#
# params = pika.URLParameters('amqps://cbrquzeq:bSGQZrdqhii4NQmaaqO6azfDbVR7VES8@shrimp.rmq.cloudamqp.com/cbrquzeq')
#
# connection = pika.BlockingConnection(params)
#
# channel = connection.channel()
#
#
# def publish(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(exchange='', routing_key='config', body=json.dumps(body), properties=properties)
