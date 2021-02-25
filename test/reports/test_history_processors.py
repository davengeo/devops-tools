from unittest.mock import MagicMock

from assertpy import assert_that

from devopstoolsdaven.reports.history_processor import history_processor_builder, HistoryProcessor


def test_history_builder_without_history():
    try:
        history_processor_builder(**{'hello': 'test'})
    except Exception as e:
        assert_that(e).is_instance_of(ValueError)


def test_history_builder_with_wrong_history_type():
    try:
        history_processor_builder(**{'history': 'test'})
    except Exception as e:
        assert_that(e).is_instance_of(ValueError)


def test_history_builder_with_history(mocker: MagicMock):
    history = mocker.patch('devopstoolsdaven.reports.history.History', autospec=True)
    history.persist = True
    processor: HistoryProcessor = history_processor_builder(**{'history': history})
    assert_that(processor).is_instance_of(HistoryProcessor)
