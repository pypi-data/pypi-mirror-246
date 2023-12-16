import datetime
import enum
import typing

import pydantic

from ...association import Association


class RepresentationModality(enum.Enum):
    RawMessage = "raw_message"
    """Render message data for any point along a topic's timeline as a JSON string."""

    TimeseriesPlot = "timeseries_plot"
    """Plot one or more message paths as lines or points."""


class RepresentationStorageFormat(enum.Enum):
    MCAP = "mcap"


class TimeseriesPlotContext(pydantic.BaseModel):
    extents: dict[str, tuple[float, float]]
    """
    [min, max] for each dimension of the data.
    Dictionary keys are message paths in dot notation (e.g., "pose.position.x").
    """


class TopicRepresentation(pydantic.BaseModel):
    """
    Pointer to Topic data processed for representation in a particular modality,
    along with any contextual metadata helpful for that representation.
    A Topic may have many representations, and several representations may make use of the same processed data.
    """

    file_id: str
    """
    A Roboto file_id.
    Representations that store data across many files should use a manifest/index file,
    to which this field should point.
    """

    context: TimeseriesPlotContext
    """
    Topic metadata useful as context to the represent the data in the specified modality.
    """

    storage_format: RepresentationStorageFormat

    modality: RepresentationModality

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enforce_invariants()

    def enforce_invariants(self):
        if self.modality == RepresentationModality.TimeseriesPlot:
            assert isinstance(self.context, TimeseriesPlotContext)
            assert self.storage_format == RepresentationStorageFormat.MCAP


class TopicSourceFile(pydantic.BaseModel):
    """
    File from which Topic data--in whole or in part--are found.
    """

    file_id: str
    """
    A Roboto file_id.
    """

    start_time: typing.Optional[str] = None
    """
    Timestamp of earliest message in topic, in nanoseconds since Unix epoch.
    """

    end_time: typing.Optional[str] = None
    """
    Timestamp of oldest message in topic, in nanoseconds since Unix epoch.
    """


class TopicRecord(pydantic.BaseModel):
    association: Association
    """
    Identifier and entity type with which this topic is associated. E.g., a dataset.
    """

    created: datetime.datetime

    frequency: int
    """
    Frequency is calculated as `1.0 / (median of time deltas between messages)`.
    This approach is used by ROS. See:
    https://github.com/ros/ros_comm/blob/noetic-devel/tools/rosbag/src/rosbag/bag.py#L882-L895.

    If frequency is calculated a different way that is trivially derived (e.g., `message_count / duration`),
    it is not worth storing as a first-class field.
    """

    name: str

    message_count: int

    message_paths: list[str]
    """
    List of dot notation paths within Topic message data to leaf values:
    ["pose.position.x", "pose.position.y", "pose.position.z"]
    """

    metadata: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    """
    Arbitrary metadata.
    """

    modified: datetime.datetime

    org_id: str

    schema_name: typing.Optional[str] = None
    """
    Type of messages in topic. E.g., "sensor_msgs/PointCloud2".
    May be None if topic does not have a known/named schema.
    """

    source_files: list[TopicSourceFile]
    """
    Recording file(s) from which this topic was extracted.
    May be more than one if recording was chunked by time or size.
    """

    representations: list[TopicRepresentation] = pydantic.Field(default_factory=list)
    """
    Zero to many representations of this topic.
    A topic will not have any representations until it has been processed.
    """
