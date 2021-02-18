from typing import Callable, Any

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
