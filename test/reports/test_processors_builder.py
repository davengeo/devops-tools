import os
import sys
from typing import Tuple, Dict

import pytest
# noinspection PyProtectedMember
from prometheus_client import push_to_gateway, REGISTRY

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from devopstoolsdaven.reports.fluentd_logger import FluentdLogger  # noqa: E402
from devopstoolsdaven.reports.logger import logger_setup, get_logger  # noqa: E402
from devopstoolsdaven.reports.history import History  # noqa: E402
from devopstoolsdaven.reports.processors_builder import get_builder_map, processors_builder  # noqa: E402
from devopstoolsdaven.reports.report import get_configuration_list, Report  # noqa: E402
from devopstoolsdaven.common.config import Config  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.wip
def test_processors_builder() -> None:
    logger_setup(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    import logging
    builder_map = get_builder_map(
        **{
            'history': History(db_path=config.get_path(key='history'),
                               context=(str({'test_method': 'test_processors_builder'}), 'pytest')),
            'logger': get_logger('app'),
            'logger.level': getattr(logging, config.get_value(section='Logging',
                                                              key='level',
                                                              default='INFO')),
            'fluentd': FluentdLogger(tag='app', label='test', host='localhost', port=24224)
        }
    )
    custom_builder_map: Tuple[Dict, ...] = tuple(
        builder_map[x] for x in builder_map.keys() if x in get_configuration_list(config=config))
    report = Report(config=config,
                    processors=processors_builder(builder_map=custom_builder_map))
    report.start()
    report.add_event_with_default_type(record={'current_test': 'test_processors_builder 1'})
    report.add_event_with_default_type(record={'current_test': 'test_processors_builder 2'})
    report.close()
    push_to_gateway('localhost:9091', job='integration-test', registry=REGISTRY)
