#!/usr/bin/env python
import pika, sys
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# fanout just broadcasts the message to all queues
channel.exchange_declare(exchange='logs', exchange_type="fanout")

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
                exchange='logs',
                routing_key='',
                body=message)
print(f" [x] Sent {message}")

connection.close()