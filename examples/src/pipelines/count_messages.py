import sys

from pypelines.kafka import OTOStatefulPipeline, KafkaSourceConfig, KafkaSinkConfig

class CountMessagesState:
    _count: int

    def __init__(self):
        self._count += 1

    def increment(self):
        self._count += 1

    @property
    def count(self):
        return self._count


class CountMessagesPipeline(OTOStatefulPipeline):
    def __init__(self):
        kafka_source_config = KafkaSourceConfig(
            bootstrap_servers="pypelines-cluster-kafka-bootstrap:9092",
            topics=["input-topic"],
        )
        kafka_sink_config = KafkaSinkConfig(
            bootstrap_servers="pypelines-cluster-kafka-bootstrap:9092",
            topic="output-topic-beam",
        )
        super().__init__(
            kafka_source_config=kafka_source_config,
            kafka_sink_config=kafka_sink_config,
        )

    def get_initial_state(self):
        return CountMessagesState()

    def get_key(self, message):
        return message["key"]

    def transform_message(self, message, state: CountMessagesState):
        state.increment()
        return {
            **message,
            "count": state.count,
        }


if __name__ == "__main__":
    pipeline = CountMessagesPipeline()
    pipeline.run(sys.argv[1:])
