from typing import Callable, Any, cast

from cloudevents.http import CloudEvent

from .history import History
from .processor import Processor


class HistoryProcessor(Processor):

    def __init__(self, history: History):
        self.__history = history

    def __str__(self) -> str:
        return "history"

    def mapper(self) -> Callable[[CloudEvent], Any]:
        return lambda x: self.__history.persist(str(x))

    def close(self) -> None:
        self.__history.close()


def history_processor_builder(**kwargs: dict) -> HistoryProcessor:
    if kwargs.get('history') is None or not hasattr(kwargs.get('history'), 'persist'):
        raise ValueError
    # noinspection PyTypeChecker
    return HistoryProcessor(cast(History, kwargs.get('history')))
