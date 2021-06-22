import logging
import time
from threading import Thread
from typing import Dict, Any, Tuple, Text, List

from cloudevents.http import CloudEvent
from prometheus_client import Counter, Summary

from .processor import Processor
from ..common.config import Config


def config2attributes(config: Config) -> Any:
    return config.get_section('CloudEvents')


def get_configuration_list(config: Config) -> Tuple[Text, ...]:
    return config.get_tuple(section='Reports', key='processors')


REQUEST_TIME = Summary('event_requesting_seconds', 'Time spent requesting event')
DELIVER_TIME = Summary('event_processing_seconds', 'Time spent processing event')
STOP = False
RUNNING = True


class Report(Thread):
    __buffer: List[CloudEvent] = []
    __state = STOP

    def __init__(self, config: Config, processors: List[Processor]):
        self.__attributes: Dict = config2attributes(config)
        self.__processors: List[Processor] = processors
        self.__c = Counter('events', 'dispatched events')
        super(Report, self).__init__(target=self.run, name='reporting')

    def register_processors(self, processors: List[Processor]) -> None:
        if self.__state == RUNNING:
            raise Exception('Register processors cannot be called after start report')
        for x in processors:
            self.__processors.append(x)

    def run(self) -> None:
        self.__state = RUNNING
        while self.__state is RUNNING:
            if len(self.__buffer) != 0:
                self.deliver_event(self.__buffer.pop(0))
            else:
                time.sleep(1)
        logging.info('finishing thread')

    @DELIVER_TIME.time()
    def deliver_event(self, event: CloudEvent) -> None:
        for x in self.__processors:
            x.mapper()(event)
        self.__c.inc()

    @REQUEST_TIME.time()
    def add_event(self, attributes: dict, record: dict) -> None:
        self.__buffer.append(CloudEvent(attributes=self.__attributes | attributes, data=record))

    def add_event_with_type(self, event_type: str, record: dict) -> None:
        return self.add_event(attributes={'type': event_type}, record=record)

    def add_event_with_default_type(self, record: dict) -> None:
        return self.add_event(attributes={}, record=record)

    def close(self) -> None:
        self.__state = STOP
        for proc in self.__processors:
            proc.close()
        self.join()
