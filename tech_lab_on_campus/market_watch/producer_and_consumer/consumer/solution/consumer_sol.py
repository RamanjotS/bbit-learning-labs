# Copyright 2024 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pika


class mqConsumerInterface:
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        connection = pika.BlockingConnection(parameters=conParams)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.exchange_declare(exchange=self.exchange_name)
        channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.binding_key,
            exchange=self.exchange_name,
        )
        channel.basic_consume(self.queue_name, self.on_message_callback, auto_ack=False)
        # channel.basic_publish(
        #     exchange=self.exchange_name,
        #     routing_key=self.binding_key,
        #     body="Message",
        # )


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