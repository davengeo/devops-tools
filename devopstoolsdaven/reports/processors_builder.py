from collections import Callable
from typing import List

from .history_processor import history_processor_builder
from .logging_processor import LoggingProcessor
from .processor import Processor


def get_builder_map() -> dict[str, Callable]:
    return {
        'history': history_processor_builder,
        'logging': LoggingProcessor
    }


def processors_builder(builder_map: dict[str, dict]) -> List[Processor]:
    result: List[Processor] = []
    for _, value in builder_map.items():
        proc_i: Callable = value.get('builder')
        kwargs_i: dict = value.get('kwargs')
        result.append(proc_i(**kwargs_i))
    return result
