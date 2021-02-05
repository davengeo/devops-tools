from typing import Dict, Any

from cloudevents.http import CloudEvent
from common.config import Config
from reports.history import History


def config2attributes(config: Config) -> Any:
    return config.get_section('CloudEvents')


class Report(object):
    def __init__(self, attributes: dict):
        self.__attributes: Dict = attributes
        self.__history: History = None

    def set_history(self, history: History):
        self.__history = history

    def add_event(self, record: dict) -> None:
        event = CloudEvent(attributes=self.__attributes, data=record)
        self.__persist(event)

    def __persist(self, event):
        if self.__history is not None:
            self.__history.persist(str(event))
