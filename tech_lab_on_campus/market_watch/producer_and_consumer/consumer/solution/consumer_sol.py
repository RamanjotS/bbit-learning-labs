import pika
import os


class mqConsumerInterface:
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel = None
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        conParams = pika.URLParameters("amqp://rabbitmq?connection_attempts=5&retry_delay=5")
        connection = pika.BlockingConnection(parameters=conParams)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.exchange_declare(exchange=self.exchange_name)
        self.channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.binding_key,
            exchange=self.exchange_name,
        )
        self.channel.basic_consume(self.queue_name, self.on_message_callback, auto_ack=False)


    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        channel.basic_ack(method_frame.delivery_tag, False)
        print(header_frame)
        print(body)

    def startConsuming(self) -> None:
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
    
    def __del__(self) -> None:
        print("Closing RMQ connection on destruction")
        self.channel.close()
        self.connection.close()


class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        super().__init__(binding_key, exchange_name, queue_name)
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.channel = None
        self.setupRMQConnection()