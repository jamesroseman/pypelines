import abc
from typing import Optional

import apache_beam as beam
from apache_beam.io import kafka
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.external import JavaJarExpansionService

from pypelines.kafka import KafkaSourceConfig, KafkaSinkConfig


class OTOStatefulPipeline(abc.ABC):
    """A one-to-one Kafka-transform-Kafka processing pipeline."""

    _kafka_source_config: KafkaSourceConfig
    _kafka_sink_config: KafkaSinkConfig
    _pipeline_options: PipelineOptions

    def __init__(
        self,
        kafka_source_config: KafkaSourceConfig,
        kafka_sink_config: KafkaSinkConfig,
        pipeline_options: Optional[PipelineOptions] = None,
    ):
        self._kafka_source_config = kafka_source_config
        self._kafka_sink_config = kafka_sink_config
        self._pipeline_options = pipeline_options or PipelineOptions()

    @staticmethod
    def _get_expansion_service(
        jar: str = "/opt/apache/beam/jars/beam-sdks-java-io-expansion-service.jar",
        args=None,
    ):
        """Gets the expansion service Jar which is packaged with Beam pipelines."""
        if args == None:
            args = [
                "--defaultEnvironmentType=PROCESS",
                '--defaultEnvironmentConfig={"command": "/opt/apache/beam/boot"}',
                "--experiments=use_deprecated_read",
            ]
        return JavaJarExpansionService(jar, ["{{PORT}}"] + args)

    @abc.abstractmethod
    def get_initial_state(self):
        """Initializes a state object, typically a class instance. The state class must be pickle-able."""
        pass

    @abc.abstractmethod
    def get_key(self, message):
        """Parses a message as a key, which is used for worker routing and state management."""
        pass

    @abc.abstractmethod
    def transform_message(self, message, state):
        """Transforms an incoming Kafka message and yields an outbound Kafka message post-transformation."""
        pass

    def run(self, argv=None):
        """Runs the Beam pipeline."""
        with beam.Pipeline(options=PipelineOptions(argv)) as pipeline:
            # Define stateful transformation
            class StatefulTransform(beam.DoFn):
                def __init__(self, outer_instance):
                    self.outer_instance = outer_instance
                    super().__init__()

                def process(self, element, state=beam.DoFn.StateParam(beam.state.ValueStateSpec("state"))):
                    key = self.outer_instance.get_key(element)
                    current_state = state.read() or self.outer_instance.get_initial_state()
                    transformed_message, new_state = self.outer_instance.transform_message(element, current_state)
                    state.write(new_state)
                    yield key, transformed_message

            # Apply transformations and write to Kafka
            (
                pipeline
                | "ReadFromKafka" >> kafka.ReadFromKafka(
                    consumer_config=self._kafka_source_config.to_config(),
                    topics=self._kafka_source_config.topics,
                    timestamp_policy=kafka.ReadFromKafka.create_time_policy,
                    commit_offset_in_finalize=True,
                    expansion_service=self._get_expansion_service(),
                )
                | "KeyByMessage" >> beam.Map(lambda message: (self.get_key(message), message))
                | "GroupByKey" >> beam.GroupByKey()
                | "TransformMessage" >> beam.ParDo(StatefulTransform(self))
                | "WriteToKafka" >> kafka.WriteToKafka(
                    producer_config=self._kafka_sink_config.to_config(),
                    topic=self._kafka_sink_config.topic,
                )
            )
