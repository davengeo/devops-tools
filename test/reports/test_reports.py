import logging
import os
import sys
from typing import Tuple, Text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devopstoolsdaven.reports.logger import logger_configurer, get_logger
from devopstoolsdaven.reports.logging_processor import LoggingProcessor
from devopstoolsdaven.reports.history_processor import HistoryProcessor
from devopstoolsdaven.reports.report import Report, config2attributes, get_configuration_list
from devopstoolsdaven.reports.history import History
from devopstoolsdaven.common.config import Config  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


def test_should_create_report() -> None:
    result: Tuple[Text] = get_configuration_list(config=config)
    print(result)
    print(locals()['result'])


def test_should_load_processors() -> None:
    hist: History = History(db_path=config.get_path(key='history'), context=(str({'example1': 'value1'}), 'test'))
    hist_proc: HistoryProcessor = HistoryProcessor(history=hist)

    logger_configurer(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    log_proc: LoggingProcessor = LoggingProcessor(logger=get_logger('app'), level=logging.WARNING)

    report = Report(config2attributes(config=config), processors=[hist_proc, log_proc])
    report.add_event(record={'hello': 'reported'})
