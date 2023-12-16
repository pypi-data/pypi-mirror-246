import typing

import pydantic

from ...association import Association
from .topic_record import (
    TopicRepresentation,
    TopicSourceFile,
)


class CreateOrUpdateTopicRequest(pydantic.BaseModel):
    """Request to memorialize a topic contained within a recording file, uploaded to a dataset."""

    # Required
    association: Association
    frequency: int
    message_count: int
    message_paths: list[str]
    topic_name: str
    source: list[TopicSourceFile]

    # Optional
    schema_name: typing.Optional[str] = None
    metadata: typing.Optional[dict[str, typing.Any]] = None
    org_id: typing.Optional[str] = None
    representations: typing.Optional[list[TopicRepresentation]] = None
