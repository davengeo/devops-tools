import logging
from logging import Logger
from typing import Callable, Any, cast

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

    def close(self) -> None:
        self.__logger.log(level=logging.INFO, msg='closing resources...')


def logging_processor_builder(**kwargs: dict) -> LoggingProcessor:
    if kwargs.get('logger') is None or not hasattr(kwargs.get('logger'), 'log') \
            or kwargs.get('level') is None or not isinstance(kwargs.get('level'), int):
        raise ValueError
    # noinspection PyTypeChecker,PyDeepBugsSwappedArgs
    return LoggingProcessor(cast(Logger, kwargs.get('logger')), cast(int, kwargs.get('level')))
