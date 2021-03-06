from typing import Callable, Any, cast

from cloudevents.http import CloudEvent

from .fluentd_logger import FluentdLogger
from .processor import Processor


class FluentdProcessor(Processor):

    def __init__(self, fluentd_logger: FluentdLogger):
        self.__fluentd_logger = fluentd_logger

    def mapper(self) -> Callable[[CloudEvent], Any]:
        return lambda x: self.__fluentd_logger.forward(x)

    def close(self) -> None:
        self.__fluentd_logger.close()


def fluentd_processor_builder(**kwargs: dict) -> FluentdProcessor:
    if kwargs.get('fluentd') is None or not hasattr(kwargs.get('fluentd'), 'forward'):
        raise ValueError
    # noinspection PyTypeChecker
    return FluentdProcessor(cast(FluentdLogger, kwargs.get('fluentd')))
