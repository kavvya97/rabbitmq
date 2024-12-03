#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# creating a temporary queue here - which generates a random name for the queue
# exclusive=True, once the connection is closed, queue should be deleted
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
# create bindings to bind the queue to the xchange
# a queue is interested in a message from this exchange
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Receiving messages works by subscribing a callback function to the queue
# when we receive the message, this callback function is called by pika library
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# this callback should receive message from <queue_name>
channel.basic_consume(queue=queue_name,
                    auto_ack=True,
                    on_message_callback=callback)

channel.start_consuming()
