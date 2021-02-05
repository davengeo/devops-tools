import os

import sys

from common.config import Config

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../devops')))
from reports.report import Report, config2attributes  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


def test_should_create_report() -> None:
    report = Report(config2attributes(config=config))
    report.add_event(record={'action': 'hello cloudEvent'})
