import abc
from typing import Generic, TypeVar

from table_data_classes import *
from database import Database
from view_data_classes import *

T = TypeVar('T')


class AbstractDatabaseAccess(abc.ABC, Generic[T]):
    def __init__(self, database_connection: Database):
        self._database: Database = database_connection

    @abc.abstractmethod
    def get_all(self) -> list[T]:
        pass


class AbstractTableAccess(AbstractDatabaseAccess, Generic[T]):
    @abc.abstractmethod
    def get_all(self) -> list[T]:
        pass


class DefaultTeamPlayerTableAccess(AbstractTableAccess[DefaultTeamPlayer]):
    def get_all(self) -> list[DefaultTeamPlayer]:
        r = self._database.execute_query("SELECT * FROM DefaultTeamPlayer")
        return [DefaultTeamPlayer(id=row[0], player=row[1], team=row[2] ) for row in r]


class GameTableAccess(AbstractTableAccess[Game]):
    def get_all(self) -> list[Game]:
        r = self._database.execute_query("SELECT * FROM Game")
        return [Game(id=row[0], team=row[1], date=row[2]) for row in r]


class GamePlayersTableAccess(AbstractTableAccess[GamePlayers]):
    def get_all(self) -> list[GamePlayers]:
        r = self._database.execute_query("SELECT * FROM GamePlayers")
        return [GamePlayers(id=row[0], game=row[1], player=row[2], paid=row[3]) for row in r]


class PenaltyTableAccess(AbstractTableAccess[Penalty]):
    def get_all(self) -> list[Penalty]:
        r = self._database.execute_query("SELECT * FROM Penalty")
        return [Penalty(id=row[0], description=row[1],
                        type=row[2], penalty=row[3],
                        lower_limit=row[4], upper_limit=row[5]) for row in r]


class PenaltyKindTableAccess(AbstractTableAccess[PenaltyKind]):
    def get_all(self) -> list[PenaltyKind]:
        r = self._database.execute_query("SELECT * FROM PenaltyKind")
        return [PenaltyKind(id=row[0], description=row[1]) for row in r]


class PlayerTableAccess(AbstractTableAccess[Player]):
    def get_all(self) -> list[Player]:
        r = self._database.execute_query("SELECT * FROM Player")
        return [Player(id=row[0], name=row[1]) for row in r]


class PlayerPenaltiesTableAccess(AbstractTableAccess[PlayerPenalties]):
    def get_all(self) -> list[PlayerPenalties]:
        r = self._database.execute_query("SELECT * FROM PlayerPenalties")
        return [PlayerPenalties(id=row[0], game_player=row[1], penalty=row[2], value=row[3]) for row in r]


class TeamTableAccess(AbstractTableAccess[Team]):
    def get_all(self) -> list[Team]:
        r = self._database.execute_query("SELECT * FROM Team")
        return [Team(id=row[0], name=row[1]) for row in r]


class TeamPenaltiesTableAccess(AbstractTableAccess[TeamPenalties]):
    def get_all(self) -> list[TeamPenalties]:
        r = self._database.execute_query("SELECT * FROM PenaltyKind")
        return [TeamPenalties(id=row[0], team=row[1], penalty=row[2]) for row in r]


class SumPerTeamViewAccess(AbstractDatabaseAccess[SumPerTeam]):
    def get_all(self) -> list[SumPerTeam]:
        r = self._database.execute_query("SELECT * FROM SumPerTeam")
        return [SumPerTeam(team_name=row[0], penalty_sum=row[1]) for row in r]


class SumPerPlayerViewAccess(AbstractDatabaseAccess[SumPerPlayer]):
    def get_all(self) -> list[SumPerPlayer]:
        r = self._database.execute_query("SELECT * FROM SumPerPlayer")
        return [SumPerPlayer(date=row[0], team=row[1], player_name=row[2], penalty=row[3]) for row in r]


if __name__ == "__main__":
    database_access = Database('strafenkatalog.db')
    tableManager = DefaultTeamPlayerTableAccess(database_access)
    result = tableManager.get_all()

    for player in result:
        print(player)

    tableManager = GameTableAccess(database_access)
    result = tableManager.get_all()

    for player in result:
        print(player)
