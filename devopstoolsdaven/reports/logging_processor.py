from logging import Logger
from typing import Callable, Any

from cloudevents.http import CloudEvent

from .processor import Processor


class LoggingProcessor(Processor):

    def __init__(self, logger: Logger, level: int):
        self.__logger: Logger = logger
        self.__level: int = level

    def __str__(self) -> str:
        return "logging"

    def mapper(self) -> Callable[[CloudEvent], Any]:
        return lambda event: self.__logger.log(level=self.__level, msg=event)


def logging_processor_builder(**kwargs: dict) -> LoggingProcessor:
    if kwargs.get('logger') is None or not hasattr(kwargs.get('logger'), 'log') \
            or kwargs.get('level') is None or not isinstance(kwargs.get('level'), int):
        raise ValueError
    # noinspection PyTypeChecker
    return LoggingProcessor(kwargs.get('logger'), kwargs.get('level'))
