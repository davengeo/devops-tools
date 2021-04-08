import json
import logging

from cloudevents.http import CloudEvent, to_json
from fluent import sender


class FluentdLogger(object):

    def __init__(self, tag: str, label: str, host: str, port: int) -> None:
        self.__sender = sender.FluentSender(tag=tag, host=host, port=port, nanosecond_precision=True)
        self.__label = label

    def forward(self, event: CloudEvent) -> None:
        data: dict = json.loads(to_json(event))
        if not self.__sender.emit(label=self.__label, data=data):
            logging.error(self.__sender.last_error)
            self.__sender.clear_last_error()

    def close(self) -> None:
        self.__sender.close()
