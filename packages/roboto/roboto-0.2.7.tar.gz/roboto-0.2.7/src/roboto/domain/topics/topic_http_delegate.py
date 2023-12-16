import typing
import urllib.parse

from ...association import Association
from ...exceptions import RobotoHttpExceptionParse
from ...http import HttpClient, roboto_headers
from .topic_delegate import TopicDelegate
from .topic_record import (
    TopicRecord,
    TopicRepresentation,
    TopicSourceFile,
)


class TopicHttpDelegate(TopicDelegate):
    __http_client: HttpClient
    __roboto_service_base_url: str

    def __init__(self, roboto_service_base_url: str, http_client: HttpClient):
        self.__http_client = http_client
        self.__roboto_service_base_url = roboto_service_base_url

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
        raise NotImplementedError("create_topic is an admin-only operation")

    def delete_topic(
        self,
        topic_name: str,
        association: Association,
        org_id: typing.Optional[str] = None,
    ) -> None:
        quoted_topic_name = urllib.parse.quote_plus(topic_name)
        encoded_association = association.url_encode()
        url = f"{self.__roboto_service_base_url}/v1/topics/association/{encoded_association}/name/{quoted_topic_name}"

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url,
                headers=roboto_headers(resource_owner_id=org_id),
            )

    def get_topic_by_name_and_association(
        self,
        topic_name: str,
        association: Association,
        org_id: typing.Optional[str] = None,
    ) -> TopicRecord:
        quoted_topic_name = urllib.parse.quote_plus(topic_name)
        encoded_association = association.url_encode()
        url = f"{self.__roboto_service_base_url}/v1/topics/association/{encoded_association}/name/{quoted_topic_name}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(
                url,
                headers=roboto_headers(resource_owner_id=org_id),
            )
        return TopicRecord.model_validate(response.from_json(json_path=["data"]))
