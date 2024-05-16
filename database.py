import sqlite3
from view_data_classes import *


class DatabaseAccess:
    def __init__(self):
        self._connection: sqlite3.Connection = sqlite3.connect('strafenkatalog.db')

    def execute_query(self, sql: str, params: tuple = ()):
        cursor = self._connection.cursor()
        return cursor.execute(sql, params).fetchall()

    def execute_command(self, sql: str, params: tuple = ()):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        self._connection.commit()


database = DatabaseAccess()
result = database.execute_query("SELECT * FROM SumPerPlayer")

player_list = [SumPerPlayer(date=row[0], team=row[1], player_name=row[2], penalty=row[3]) for row in result]
print(player_list)

