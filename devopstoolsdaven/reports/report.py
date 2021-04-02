from typing import Dict, Any, Tuple, Text, List

from cloudevents.http import CloudEvent
from prometheus_client import Counter, Summary

from .processor import Processor
from ..common.config import Config


def config2attributes(config: Config) -> Any:
    return config.get_section('CloudEvents')


def get_configuration_list(config: Config) -> Tuple[Text, ...]:
    return config.get_tuple(section='Reports', key='processors')


REQUEST_TIME = Summary('event_processing_seconds', 'Time spent processing event')


class Report(object):

    def __init__(self, attributes: dict, processors: List[Processor]):
        self.__attributes: Dict = attributes
        self.__processors: List[Processor] = processors
        self.__c = Counter('events', 'dispatched events')

    @REQUEST_TIME.time()
    def add_event(self, record: dict) -> None:
        event: CloudEvent = CloudEvent(attributes=self.__attributes, data=record)
        for x in self.__processors:
            x.mapper()(event)
        self.__c.inc()

    def close(self) -> None:
        for proc in self.__processors:
            proc.close()
