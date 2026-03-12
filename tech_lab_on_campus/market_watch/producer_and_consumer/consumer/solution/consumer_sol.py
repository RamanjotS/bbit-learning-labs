from ..consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        # super().__init__(binding_key, exchange_name, queue_name)
        binding_key = binding_key
        exchange_name = exchange_name
        queue_name = queue_name
        self.setupRMQConnection()
