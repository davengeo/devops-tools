# import os
# from unittest.mock import MagicMock, call, mock_open, patch
#
# import sys
# from assertpy import assert_that
#
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../devops')))
# from reports.report import Report  # noqa: E402
# from reports.history import History  # noqa: E402
#
#
# def test_should_initialise_db(mocker: MagicMock) -> None:
#     conn = MagicMock()
#     cur = MagicMock()
#     conn.cursor.return_value = cur
#     cur.fetchone.return_value = None
#     patch_sql = mocker.patch('sqlite3.connect', return_value=conn)
#     History(hist_path='.', db_name='test')
#     patch_sql.assert_called_once()
#     conn.cursor.assert_called_once()
#     # noinspection SqlResolve,SqlNoDataSourceInspection
#     calls = [call('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ('History',)),
#              call('''CREATE TABLE History (id INTEGER PRIMARY KEY,  input_file varchar(80) NOT NULL,
#                  output_file varchar(80), environment varchar(20), timestamp DATETIME, user varchar(20))''')]
#     cur.execute.assert_has_calls(calls=calls, any_order=False)
#
#
# def test_should_not_initialise_db(mocker: MagicMock) -> None:
#     conn = MagicMock()
#     cur = MagicMock()
#     conn.cursor.return_value = cur
#     cur.fetchone.return_value = []
#     patch_sql = mocker.patch('sqlite3.connect', return_value=conn)
#     History(hist_path='.', db_name='test')
#     patch_sql.assert_called_once()
#     conn.cursor.assert_called_once()
#     # noinspection SqlResolve
#     calls = [call('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ('History',))]
#     cur.execute.assert_has_calls(calls=calls, any_order=False)
#
#
# def test_should_create_record(mocker: MagicMock) -> None:
#     conn = MagicMock()
#     cur = MagicMock()
#     conn.cursor.return_value = cur
#     cur.fetchone.return_value = []
#     mocker.patch('sqlite3.connect', return_value=conn)
#     history = History(hist_path='.', db_name='test')
#     report = Report()
#     report.append_event(name='test-record', record={'hello': 'test'})
#     m = mock_open()
#     # noinspection PyDeepBugsSwappedArgs
#     with patch('{}.open'.format('reports.history'), m):
#         history.save_report(report=report, input_data='test', env='test')
#     assert_that(m.call_args_list).is_length(2)
