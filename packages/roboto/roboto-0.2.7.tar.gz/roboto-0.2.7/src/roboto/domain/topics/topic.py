import typing

from ...association import Association
from ...serde import pydantic_jsonable_dict
from .topic_delegate import TopicDelegate
from .topic_record import (
    TopicRecord,
    TopicRepresentation,
    TopicSourceFile,
)


class Topic:
    __delegate: TopicDelegate
    __record: TopicRecord

    @classmethod
    def create_or_update(
        cls,
        # Required
        association: Association,
        frequency: int,
        message_count: int,
        message_paths: list[str],
        topic_name: str,
        source: list[TopicSourceFile],
        topic_delegate: TopicDelegate,
        # Optional
        schema_name: typing.Optional[str] = None,
        metadata: typing.Optional[dict[str, typing.Any]] = None,
        org_id: typing.Optional[str] = None,
        representations: typing.Optional[list[TopicRepresentation]] = None,
    ) -> "Topic":
        """
        Topics are uniquely identified by their name and association.
        If a Topic with the given name and association already exists, it will be updated:
            - `source` will be appended to existing TopicRecord::source_files
            - `representations`, if provided, will be appended to existing TopicRecord::representations
            - All other provided fields will overwrite existing values
        """
        record = topic_delegate.create_or_update_topic(
            association=association,
            topic_name=topic_name,
            source=source,
            frequency=frequency,
            schema_name=schema_name,
            message_count=message_count,
            message_paths=message_paths,
            metadata=metadata,
            org_id=org_id,
            representations=representations,
        )
        return cls(record, topic_delegate)

    @classmethod
    def from_name_and_association(
        cls,
        topic_name: str,
        association: Association,
        topic_delegate: TopicDelegate,
        org_id: typing.Optional[str] = None,
    ) -> "Topic":
        return cls(
            record=topic_delegate.get_topic_by_name_and_association(
                topic_name=topic_name,
                association=association,
                org_id=org_id,
            ),
            delegate=topic_delegate,
        )

    def __init__(self, record: TopicRecord, delegate: TopicDelegate):
        self.__record = record
        self.__delegate = delegate

    @property
    def record(self) -> TopicRecord:
        return self.__record

    def delete(self) -> None:
        self.__delegate.delete_topic(
            topic_name=self.__record.name,
            association=self.__record.association,
            org_id=self.__record.org_id,
        )

    def to_dict(self) -> dict[str, typing.Any]:
        return pydantic_jsonable_dict(self.__record)
