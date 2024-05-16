import abc
from typing import Generic, TypeVar

from table_data_classes import *
from database import DatabaseAccess

T = TypeVar('T')


class AbstractTableManager(abc.ABC, Generic[T]):
    def __init__(self, database_connection: DatabaseAccess):
        self._database: DatabaseAccess = database_connection

    @abc.abstractmethod
    def get_all(self) -> list[T]:
        pass


class DefaultTeamPlayerTableManager(AbstractTableManager[DefaultTeamPlayer]):
    def get_all(self) -> list[DefaultTeamPlayer]:
        r = self._database.execute_query("SELECT * FROM DefaultTeamPlayer")
        return [DefaultTeamPlayer(id=row[0], player=row[1], team=row[2] ) for row in r]


class GameTableManager(AbstractTableManager[Game]):
    def get_all(self) -> list[Game]:
        r = self._database.execute_query("SELECT * FROM Game")
        return [Game(id=row[0], team=row[1], date=row[2]) for row in r]


class GamePlayersTableManager(AbstractTableManager[GamePlayers]):
    def get_all(self) -> list[GamePlayers]:
        r = self._database.execute_query("SELECT * FROM GamePlayers")
        return [GamePlayers(id=row[0], game=row[1], player=row[2], paid=row[3]) for row in r]


class PenaltyTableManager(AbstractTableManager[Penalty]):
    def get_all(self) -> list[Penalty]:
        r = self._database.execute_query("SELECT * FROM Penalty")
        return [Penalty(id=row[0], description=row[1],
                        type=row[2], penalty=row[3],
                        lower_limit=row[4], upper_limit=row[5]) for row in r]


class PenaltyKindTableManager(AbstractTableManager[PenaltyKind]):
    def get_all(self) -> list[PenaltyKind]:
        r = self._database.execute_query("SELECT * FROM PenaltyKind")
        return [PenaltyKind(id=row[0], description=row[1]) for row in r]


class PlayerTableManager(AbstractTableManager):
    def get_all(self):
        pass


class PlayerPenaltiesTableManager(AbstractTableManager):
    def get_all(self):
        pass


class TeamTableManager(AbstractTableManager):
    def get_all(self):
        pass


class TeamPenaltiesTableManager(AbstractTableManager):
    def get_all(self):
        pass


database_access = DatabaseAccess()
tableManager = DefaultTeamPlayerTableManager(database_access)
result = tableManager.get_all()

for player in result:
    print(player)

tableManager = GameTableManager(database_access)
result = tableManager.get_all()

for player in result:
    print(player)