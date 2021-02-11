import logging
import os
import sys

from assertpy import assert_that, fail

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devopstoolsdaven.common.config import Config  # noqa: E402


def test_should_get_config_for_logging_level() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    logging_level = config.get_value('logging', 'logging_level')
    assert_that(logging_level).is_equal_to('DEBUG')
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
    logging.debug('testing config files')


def test_should_get_config_for_config_files() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    assert_that(config.get_path('configuration')).ends_with('/devops-tools/config')


def test_should_raise_exception_if_key_not_found() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    try:
        config.get_path('no_existing_key')
        fail('it should raise exception')
    except KeyError as e:
        assert_that(e.args[0]).is_equal_to('no_existing_key')


def test_should_get_json_content_for_config_files() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    assert_that(config.get_json_file('configuration', 'example/example.json')) \
        .is_equal_to({'example': 'nostradamus'})
