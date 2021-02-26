import logging
import os
import sys
from typing import List

import pytest



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from devopstoolsdaven.reports.processors_builder import get_builder_map, processors_builder
from devopstoolsdaven.reports.logger import logger_configurer, get_logger
from devopstoolsdaven.reports.history import History
from devopstoolsdaven.common.config import Config
from devopstoolsdaven.reports.processor import Processor
from devopstoolsdaven.reports.report import Report, config2attributes

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.wip
def test_processors_builder():
    logger_configurer(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    custom_builder_map: dict = {
        'history': {
            'builder': get_builder_map().get('history'),
            'kwargs': {
                'history': History(db_path=config.get_path(key='history'),
                                   context=(str({'example1': 'value1'}), 'test'))
            }
        },
        'logging': {
            'builder': get_builder_map().get('logging'),
            'kwargs': {
                'logger': get_logger(name='app'),
                'level': logging.INFO
            }
        }
    }
    processors: List[Processor] = processors_builder(custom_builder_map)
    report = Report(config2attributes(config=config), processors=processors)
    report.add_event(record={'current_test': 'test_processors_builder'})
