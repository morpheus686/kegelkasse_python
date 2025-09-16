import sqlite3
from typing import Any
import aiosqlite


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

    async def execute_query_async(self, sql: str, params: tuple = ()):
        async with aiosqlite.connect(self._db_name) as db:
            async with db.execute(sql, params) as cursor:
                return await cursor.fetchall()

    async def execute_single_query_async(self, sql: str, params: tuple = ()):
        async with aiosqlite.connect(self._db_name) as db:
            async with db.execute(sql, params) as cursor:
                return await cursor.fetchone()

    async def execute_command_async(self, sql: str, params: tuple = ()):
        async with aiosqlite.connect(self._db_name) as db:
            await db.execute(sql, params)
            await db.commit()