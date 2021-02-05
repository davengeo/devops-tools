import getpass
import logging
import sqlite3
from datetime import datetime
from typing import Tuple, Text


class History(object):
    __current: int = None

    def __init__(self, db_path: str, context: Tuple[Text, Text]) -> None:
        self.__conn = sqlite3.connect(db_path)
        self.__initialise_tables()
        self.__initialise_current(context=context)

    def __initialise_current(self, context: Tuple[Text, Text]):
        c = self.__conn.cursor()
        c.execute('''UPDATE Executions SET current=? WHERE current=?''', (0, 1))
        c.execute(
            '''INSERT INTO Executions(input_file, environment, timestamp, user, current) VALUES (?, ?, ?, ?, ?)''',
            (context[0], context[1], datetime.now(), getpass.getuser(), 1))
        self.__conn.commit()
        logging.info('current execution added to history db.')

    def __initialise_tables(self):
        c = self.__conn.cursor()
        c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ('Executions',))
        if c.fetchone() is None:
            c.execute(
                '''CREATE TABLE Executions (id INTEGER PRIMARY KEY,  input_file TEXT NOT NULL,
                    environment varchar(20), timestamp DATETIME, user TEXT, current INTEGER)''')
            c.execute('''CREATE TABLE Logs (id INTEGER PRIMARY KEY, executionId INTEGER NOT NULL, record TEXT NOT 
            NULL)''')
        self.__conn.commit()
        logging.info('history db initialised.')

    def get_current(self) -> int:
        if self.__current is None:
            self.__current = self.__get_current_from_db()
        return self.__current

    def __get_current_from_db(self) -> int:
        c = self.__conn.cursor()
        c.execute('''SELECT id FROM Executions WHERE current=?''', (1,))
        row = c.fetchone()
        if row is None:
            raise StateError(message='No current execution in history db')
        return row[0]

    def persist(self, event: str):
        c = self.__conn.cursor()
        c.execute('''INSERT INTO Logs(executionId, record) VALUES (?, ?)''', (self.get_current(), event))
        self.__conn.commit()


class StateError(BaseException):
    def __init__(self, message: str):
        self.message = message
