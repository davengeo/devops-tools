import logging
import os
import sys
import time

import pytest
from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from devopstoolsdaven.common.config import Config
from devopstoolsdaven.container import Container
from devopstoolsdaven.reports.logger import logger_setup, get_logger
from devopstoolsdaven.reports.logging_processor import LoggingProcessor
from devopstoolsdaven.reports.report import Report


@pytest.mark.wip
def test_should_instantiate_config_from_di_container() -> None:
    container: Container = Container(
        config_dependency=Config(path_file=os.path.join(os.path.dirname(__file__), '../app.ini'))
    )
    config: Config = container.config_dependency()
    assert_that(config.get_value('Logging', 'level')).is_equal_to('INFO')


@pytest.mark.wip
def test_should_instantiate_report_from_di_container() -> None:
    container: Container = Container(
        config_dependency=Config(path_file=os.path.join(os.path.dirname(__file__), '../app.ini'))
    )
    config: Config = container.config_dependency()
    logger_setup(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    log_proc: LoggingProcessor = LoggingProcessor(logger=get_logger('app'), level=logging.WARNING)
    report: Report = container.report_service()
    report.register_processors([log_proc])
    report.start()
    report.add_event_with_type(event_type='testing event', record={
        'method': 'test_should_instantiate_report_from_DI_container'
    })
    time.sleep(2)
    report.close()
