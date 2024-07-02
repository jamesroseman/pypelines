import dataclasses
from typing import Any, List, Optional


@dataclasses.dataclass
class KafkaConfig:
    bootstrap_servers: str
    auto_offset_reset: Optional[str] = None
    group_id: Optional[str] = None

    def to_config(self) -> dict[str, Any]:
        config = {
            "bootstrap.servers": self.bootstrap_servers,
        }
        if self.auto_offset_reset is not None:
            config["auto.offset.reset"] = "latest"
        if self.group_id is not None:
            config["group.id"] = self.group_id
        return config


@dataclasses.dataclass(kw_only=True)
class KafkaSourceConfig(KafkaConfig):
    topics: List[str]
    key_deserializer: str = "org.apache.kafka.common.serialization.StringDeserializer"
    value_deserializer: str = "org.apache.kafka.connect.json.JsonDeserializer"

    def to_config(self) -> dict[str, Any]:
        return {
            **super().to_config(),
            "key.deserializer": self.key_deserializer,
            "value.deserializer": self.value_deserializer,
        }


@dataclasses.dataclass(kw_only=True)
class KafkaSinkConfig(KafkaConfig):
    topic: str
    key_serializer: str = "org.apache.kafka.common.serialization.StringSerializer"
    value_serializer: str = "org.apache.kafka.connect.json.JsonSerializer"

    def to_config(self) -> dict[str, Any]:
        return {
            **super().to_config(),
            "key.serializer": self.key_serializer,
            "value.serializer": self.value_serializer,
        }
