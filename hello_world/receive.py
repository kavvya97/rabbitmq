import pika,sys,os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # can be avoided if the queue exists. else this will create a new queue for you
    # for ex, if we are not sure which program to run first
    channel.queue_declare(queue='message_queue')

    # Receiving messages works by subscribing a callback function to the queue
    # when we receive the message, this callback function is called by pika library
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")


    # this callback should receive message from <queue_name>
    channel.basic_consume(queue='message_queue',
                        auto_ack=True,
                        on_message_callback=callback)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Go into never-ending loop and waits for data and runs callback when necessary
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)