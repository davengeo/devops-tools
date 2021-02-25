from collections import Callable

from .history_processor import HistoryProcessor
from .logging_processor import LoggingProcessor

builders_map: dict[str, Callable] = {
    'history': HistoryProcessor,
    'logging': LoggingProcessor
}


def processors_builder():
    pass
