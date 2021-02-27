import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from devopstoolsdaven.reports.logger import logger_setup, get_logger
from devopstoolsdaven.reports.history import History
from devopstoolsdaven.reports.processors_builder import get_builder_map, processors_builder
from devopstoolsdaven.reports.report import get_configuration_list, Report, config2attributes
from devopstoolsdaven.common.config import Config

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.wip
def test_processors_builder():
    logger_setup(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    builder_map = get_builder_map(
        **{'history': History(db_path=config.get_path(key='history'),
                              context=(str({'test_method': 'test_processors_builder'}), 'pytest')),
           'logger': get_logger('app'),
           'logger.level': getattr(logging, config.get_value(section='Logging',
                                                             key='level',
                                                             default='INFO'))
           }
    )
    custom_builder_map = tuple(builder_map[x]
                               for x in builder_map.keys() if x in get_configuration_list(config=config))
    report = Report(config2attributes(config=config), processors=processors_builder(builder_map=custom_builder_map))
    report.add_event(record={'current_test': 'test_processors_builder'})
