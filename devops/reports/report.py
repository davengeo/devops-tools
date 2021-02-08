import logging
from typing import Dict, Any

from cloudevents.http import CloudEvent

from .history import History
from ..common.config import Config


def config2attributes(config: Config) -> Any:
    return config.get_section('CloudEvents')


class Report(object):
    def __init__(self, attributes: dict, history: History):
        self.__attributes: Dict = attributes
        self.__history = history

    def add_event(self, record: dict) -> None:
        event = CloudEvent(attributes=self.__attributes, data=record)
        logging.info(str(event))
        self.__history.persist(event=str(event))
