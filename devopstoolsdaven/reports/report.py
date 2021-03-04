from typing import Dict, Any, Tuple, Text, List

from cloudevents.http import CloudEvent

from .processor import Processor
from ..common.config import Config


def config2attributes(config: Config) -> Any:
    return config.get_section('CloudEvents')


def get_configuration_list(config: Config) -> Tuple[Text, ...]:
    return config.get_tuple(section='Reports', key='processors')


class Report(object):
    def __init__(self, attributes: dict, processors: List[Processor]):
        self.__attributes: Dict = attributes
        self.__processors: List[Processor] = processors

    def add_event(self, record: dict) -> None:
        event: CloudEvent = CloudEvent(attributes=self.__attributes, data=record)
        for x in self.__processors:
            x.mapper()(event)

    def close(self) -> None:
        for proc in self.__processors:
            proc.close()
