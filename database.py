import sqlite3
from typing import Any
from contextlib import contextmanager


class Database:
    def __init__(self, db_name: str):
        self._connection: sqlite3.Connection = sqlite3.connect(db_name)

    @property
    def in_transaction(self) -> bool:
        return self._connection.in_transaction

    def execute_query(self, sql: str, params: tuple = ()):
        cursor = self._connection.cursor()
        return cursor.execute(sql, params).fetchall()

    def execute_single_query(self, sql: str, params: tuple = ()) -> Any:
        cursor = self._connection.cursor()
        return cursor.execute(sql, params).fetchone()

    def execute_command(self, sql: str, params: tuple = ()):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        return cursor.lastrowid
          
    @contextmanager
    def transaction(self):
        try:
            self._connection.execute("BEGIN")
            yield
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise
