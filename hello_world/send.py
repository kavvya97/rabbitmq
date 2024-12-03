#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
message = "Hello World!"
# named queue 
queue_name = "message_queue"
channel.queue_declare(queue=queue_name)

# queue name has to be present in routing key parameter
channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      message='Hello World!')

connection.close()

