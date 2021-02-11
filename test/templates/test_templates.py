import os
import sys

import pytest
from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from devopstoolsdaven.templates.templates import Templates  # noqa: E402
from devopstoolsdaven.common.config import Config  # noqa: E402

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


@pytest.mark.integration
def test_render_a_simple_template() -> None:
    templates = Templates(config)
    result = templates.render(template_name='hello_world', data={'mustache': 'Unit test'})
    assert_that(result).is_equal_to('Hello, Unit test!')
