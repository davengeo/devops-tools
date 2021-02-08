import os
import sys
from typing import Text

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devops.common.config import Config  # noqa: E402
from devops.reports.history import History  # noqa: E402
from devops.reports.report import Report, config2attributes  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.integration
def test_should_initialise_db() -> None:
    input_file: Text = str({'param1': 'value1'})
    history = History(db_path=config.get_path(key='history'), context=(input_file, 'test'))
    report = Report(config2attributes(config=config), history=history)
    report.add_event(record={'action': 'new cloudEvent from integration test'})
