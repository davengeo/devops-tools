import logging
import os
import sys
from typing import Tuple

import pytest

from ..common.register_hook import unregister_metrics

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devopstoolsdaven.reports.logger import logger_setup, get_logger  # noqa: E402
from devopstoolsdaven.reports.logging_processor import LoggingProcessor  # noqa: E402
from devopstoolsdaven.reports.history_processor import HistoryProcessor  # noqa: E402
from devopstoolsdaven.reports.report import Report, config2attributes, get_configuration_list  # noqa: E402
from devopstoolsdaven.reports.history import History  # noqa: E402
from devopstoolsdaven.common.config import Config  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


def test_should_create_report() -> None:
    result: Tuple[str, ...] = get_configuration_list(config=config)
    print(result)
    print(locals()['result'])


@pytest.mark.wip
def test_should_load_processors() -> None:
    unregister_metrics()
    hist: History = History(db_path=config.get_path(key='history'), context=(str({'example1': 'value1'}), 'test'))
    hist_proc: HistoryProcessor = HistoryProcessor(history=hist)

    logger_setup(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    log_proc: LoggingProcessor = LoggingProcessor(logger=get_logger('app'), level=logging.WARNING)

    report = Report(config2attributes(config=config), processors=[hist_proc, log_proc])
    report.add_event_with_type(event_type='test-in-library', record={'hello': 'reported'})
    report.add_event_with_default_type(record={'hello': 'reported'})
    report.add_event(attributes={'extra': 'hello'}, record={'hello': 'reported'})
