import pika,sys,os, time


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# can be avoided if the queue exists. else this will create a new queue for you
# for ex, if we are not sure which program to run first
channel.queue_declare(queue='task_queue')

# Receiving messages works by subscribing a callback function to the queue
# when we receive the message, this callback function is called by pika library

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)

# this callback should receive message from <queue_name>
channel.basic_consume(queue='task_queue',
                    on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


