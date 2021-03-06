import os
import sys

from assertpy import assert_that, fail

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devopstoolsdaven.common.config import Config  # noqa: E402


def test_should_get_config_for_config_folder() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    config_folder = config.get_value('Paths', 'configuration')
    assert_that(config_folder).is_equal_to('./config')


def test_should_get_config_for_config_files() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    assert_that(config.get_path('configuration')).ends_with('/devops-tools/config')


def test_should_raise_exception_whether_key_not_found() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    try:
        config.get_path('no_existing_key')
        fail('it should raise exception')
    except KeyError as e:
        assert_that(e.args[0]).is_equal_to('no_existing_key')


def test_should_return_default_value_whether_key_not_found() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    try:
        value = config.get_value(section='Paths', key='no_existing_key', default='DEFAULT')
        assert_that(value).is_equal_to('DEFAULT')
    except KeyError as e:
        fail('it should not raise exception {}'.format(e))


def test_should_get_json_content_for_config_files() -> None:
    config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))
    assert_that(config.get_json_file('configuration', 'example/example.json')) \
        .is_equal_to({'example': 'nostradamus'})
