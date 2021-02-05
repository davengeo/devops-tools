import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../devops')))
from reports.report import Report, config2attributes
from common.config import Config  # noqa: E402
from reports.history import History  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.integration
def test_should_initialise_db() -> None:
    history = History(db_path=config.get_path(key='history'), context=('input file', 'test'))
    report = Report(config2attributes(config=config))
    report.set_history(history=history)
    report.add_event(record={'action': 'hello cloudEvent'})
