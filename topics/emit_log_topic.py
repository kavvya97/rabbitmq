#!/usr/bin/env python
import pika, sys
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

'''
Filtering not just based on severity but also facility
auth/cron/kern...
typhicaly using a delimiter * or #
a message sent with a particular routing key will be delivered to all the queues 
that are bound with a matching binding key. However there are two important special
cases for binding keys:

* (star) can substitute for exactly one word.
# (hash) can substitute for zero or more words.
'''
channel.exchange_declare(exchange='topic_logs', exchange_type="topic")

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='topic_logs',routing_key=routing_key,body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()

