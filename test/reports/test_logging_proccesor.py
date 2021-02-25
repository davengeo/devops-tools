import os
import sys
from logging import Logger

import pytest
from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from devopstoolsdaven.common.config import Config  # noqa: E402
from devopstoolsdaven.reports.logging_processor import logging_processor_builder, LoggingProcessor  # noqa: E402
from devopstoolsdaven.reports.logger import logger_configurer, get_logger  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.wip
def test_logging_builder_without_logging():
    try:
        logging_processor_builder(**{'hello': 'test'})
    except Exception as e:
        assert_that(e).is_instance_of(ValueError)


@pytest.mark.wip
def test_logging_builder_with_wrong_logging_type():
    try:
        logging_processor_builder(**{'logger': 'test', 'level': 1})
    except Exception as e:
        assert_that(e).is_instance_of(ValueError)


@pytest.mark.wip
def test_logging_builder_with_logger():
    logger_configurer(log_cfg=config.get_yaml_file(key='configuration', file_name='logging.yml'))
    logging: Logger = get_logger(name='app')
    processor: LoggingProcessor = logging_processor_builder(**{'logger': logging, 'level': 1})
    assert_that(processor).is_instance_of(LoggingProcessor)
