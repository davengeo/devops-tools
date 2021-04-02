from collections import Callable
from typing import List, Tuple, cast, Dict

from .fluentd_processor import fluentd_processor_builder
from .history_processor import history_processor_builder
from .logging_processor import logging_processor_builder
from .processor import Processor


def get_builder_map(**kwargs: dict) -> dict[str, dict]:
    return {
        'history': {
            'builder': history_processor_builder,
            'kwargs': {
                'history': kwargs.get('history')
            }
        },
        'logging': {
            'builder': logging_processor_builder,
            'kwargs': {
                'logger': kwargs.get('logger'),
                'level': kwargs.get('logger.level')
            }
        },
        'fluentd': {
            'builder': fluentd_processor_builder,
            'kwargs': {
                'fluentd': kwargs.get('fluentd')
            }
        }
    }


def processors_builder(builder_map: Tuple[Dict, ...]) -> List[Processor]:
    result: List[Processor] = []
    for item in builder_map:
        proc_i: Callable = cast(Callable, item.get('builder'))
        # noinspection PyDeepBugsSwappedArgs
        kwargs_i: dict = cast(dict, item.get('kwargs'))
        result.append(proc_i(**kwargs_i))
    return result
