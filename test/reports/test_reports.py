import os

import sys
from unittest.mock import MagicMock, ANY

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devopstoolsdaven.common.config import Config  # noqa: E402
from devopstoolsdaven.reports.history import History  # noqa: E402
from devopstoolsdaven.reports.report import Report, config2attributes  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


def test_should_create_report() -> None:
    hist: History = MagicMock()
    report = Report(config2attributes(config=config), history=hist)
    report.add_event(record={'action': 'new cloudEvent from unit test'})
    hist.persist.assert_called_with(event=ANY)
