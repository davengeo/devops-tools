import os
import sys
import time
from typing import Text

import pytest
from assertpy import assert_that, fail

from .common.register_hook import unregister_metrics

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from devopstoolsdaven.container import Container  # noqa: E402
from devopstoolsdaven.reports.report import Report  # noqa: E402
from devopstoolsdaven.vault.vault import Vault  # noqa: E402


@pytest.mark.wip
def test_should_instantiate_config_from_di_container() -> None:
    container: Container = Container()
    container.config.from_ini(os.path.join(os.path.dirname(__file__), '../app.ini'))
    assert_that(container.config.logging()['level']).is_instance_of(Text)


@pytest.mark.wip
def test_should_instantiate_templates_from_di_container() -> None:
    container: Container = Container()
    container.config.from_ini(os.path.join(os.path.dirname(__file__), '../app.ini'))
    templates = container.template_service()
    result = templates.render(template_name='hello_world', data={'mustache': 'Unit test'})
    assert_that(result).is_equal_to('Hello, Unit test!')


@pytest.mark.wip
def test_should_instantiate_report_from_di_container() -> None:
    unregister_metrics()
    container: Container = Container()
    container.config.from_ini(os.path.join(os.path.dirname(__file__), '../app.ini'))
    container.init_resources()
    report: Report = container.report_service()
    assert_that(report.is_alive()).is_true()
    report.add_event_with_type(event_type='testing event', record={
        'method': 'test_should_instantiate_report_from_DI_container'
    })
    time.sleep(2)
    container.shutdown_resources()


@pytest.mark.wip
def test_should_instantiate_vault_from_di_container() -> None:
    unregister_metrics()
    container: Container = Container()
    container.config.from_ini(os.path.join(os.path.dirname(__file__), '../app.ini'))
    container.init_resources()
    vault: Vault = container.vault_service()
    if vault.is_authenticated():
        assert_that(vault.read_secret('test')).is_equal_to({'test': 'OK'})
    else:
        fail()(msg='should be authenticated')
    container.shutdown_resources()
