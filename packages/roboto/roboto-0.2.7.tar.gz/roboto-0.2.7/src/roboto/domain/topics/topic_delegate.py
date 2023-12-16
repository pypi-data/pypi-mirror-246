import abc
import typing

from ...association import Association
from .topic_record import (
    TopicRecord,
    TopicRepresentation,
    TopicSourceFile,
)


class TopicDelegate(abc.ABC):
    @abc.abstractmethod
    def create_or_update_topic(
        self,
        # Required
        association: Association,
        frequency: int,
        message_count: int,
        message_paths: list[str],
        topic_name: str,
        source: list[TopicSourceFile],
        # Optional
        schema_name: typing.Optional[str] = None,
        metadata: typing.Optional[dict[str, typing.Any]] = None,
        org_id: typing.Optional[str] = None,
        representations: typing.Optional[list[TopicRepresentation]] = None,
    ) -> TopicRecord:
        raise NotImplementedError("create_topic")

    @abc.abstractmethod
    def delete_topic(
        self,
        topic_name: str,
        association: Association,
        org_id: typing.Optional[str] = None,
    ) -> None:
        raise NotImplementedError("delete_topic")

    @abc.abstractmethod
    def get_topic_by_name_and_association(
        self,
        topic_name: str,
        association: Association,
        org_id: typing.Optional[str] = None,
    ) -> TopicRecord:
        raise NotImplementedError("get_topic_by_name_and_dataset")
