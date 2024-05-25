import sqlite3
from typing import Any
from view_data_classes import *


class Database:
    def __init__(self, db_name: str):
        self._connection: sqlite3.Connection = sqlite3.connect(db_name)

    def execute_query(self, sql: str, params: tuple = ()):
        cursor = self._connection.cursor()
        return cursor.execute(sql, params).fetchall()

    def execute_single_query(self, sql: str, params: tuple = ()) -> Any:
        cursor = self._connection.cursor()
        return cursor.execute(sql, params).fetchone()

    def execute_command(self, sql: str, params: tuple = ()):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        self._connection.commit()
