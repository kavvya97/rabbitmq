#!/usr/bin/env python
import pika, sys
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

'''
A binding is a relationship between an exchange and a queue.
Bindings can take an extra routing_key parameter. 
This helps to filter messages based on its severity

'''
channel.exchange_declare(exchange='direct_logs', exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# routing_key = info/error/warn here. 
# Now inorder to filter the messsages at receiver, we need to ensure the receiver binding key 
# matches the routing key here
channel.basic_publish(exchange='direct_logs',routing_key=severity,body=message)
print(f" [x] Sent {severity}:{message}")
connection.close()

