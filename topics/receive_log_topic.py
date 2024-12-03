#!/usr/bin/env python
import pika, sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
binding_key = sys.argv[1:]

if not binding_key:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for binding in binding_key:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Receiving messages works by subscribing a callback function to the queue
# when we receive the message, this callback function is called by pika library
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
