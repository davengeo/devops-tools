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
        return lambda x: self.__logger.log(level=self.__level, msg=x)
