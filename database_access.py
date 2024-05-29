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
        return [DefaultTeamPlayer(id=row[0], player=row[1], team=row[2]) for row in r]


class GameTableAccess(AbstractTableAccess[Game]):
    def get_all(self) -> list[Game]:
        r = self._database.execute_query("SELECT * FROM Game")
        return [Game(id=row[0], team=row[1], date=row[2]) for row in r]


class GamePlayerTableAccess(AbstractTableAccess[GamePlayers]):
    def get_all(self) -> list[GamePlayers]:
        r = self._database.execute_query("SELECT * FROM GamePlayers")
        return [GamePlayers(id=r[0], game=r[1], player=r[2],
                            paid=r[3], sum_points=r[4], full=r[5],
                            clear=r[6], errors=r[7]) for row in r]

    def get_by_game_and_player(self, game_id: int, player_id: int) -> GamePlayers:
        query = "SELECT * FROM GamePlayers WHERE Game = ? AND Player = ?"
        params = (game_id, player_id)
        r = self._database.execute_single_query(query, params)

        return GamePlayers(id=r[0], game=r[1], player=r[2],
                           paid=r[3], sum_points=r[4], full=r[5],
                           clear=r[6], errors=r[7])

    def update(self, game_player: GamePlayers) -> None:
        query = """UPDATE GamePlayers 
                   SET Result = ?,
                       Full = ?,
                       Clear = ?,
                       Errors = ?
                   WHERE Id = ?"""

        params = (game_player.sum_points, game_player.full, game_player.clear, game_player.errors, game_player.id)
        self._database.execute_command(query, params)


class PenaltyTableAccess(AbstractTableAccess[Penalty]):
    def get_all(self) -> list[Penalty]:
        r = self._database.execute_query("SELECT * FROM Penalty")
        return [Penalty(id=row[0], description=row[1],
                        type=row[2], penalty=row[3],
                        lower_limit=row[4], upper_limit=row[5],
                        get_value_by_parent=row[6]) for row in r]

    def get_by_id(self, penalty_id: int) -> Penalty:
        query = "SELECT * FROM Penalty WHERE Id = ?"
        params = (penalty_id,)
        r = self._database.execute_single_query(query, params)

        return Penalty(id=r[0], description=r[1],
                       type=r[2], penalty=r[3],
                       lower_limit=r[4], upper_limit=r[5],
                       get_value_by_parent=r[6])


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

    def get_by_gameplayerid(self, gameplayerid: int) -> list[PlayerPenalties]:
        query = "SELECT * FROM PlayerPenalties WHERE GamePlayer = ?"
        params = (gameplayerid,)
        r = self._database.execute_query(query, params)

        return [PlayerPenalties(id=row[0], game_player=row[1], penalty=row[2], value=row[3]) for row in r]

    def update(self, player_penalty: PlayerPenalties):
        query = """UPDATE PlayerPenalties 
                   SET Value = ?
                   WHERE Id = ?"""

        params = (player_penalty.value, player_penalty.id)
        self._database.execute_command(query, params)


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
        return self._create_sumperplayer_list(r)

    def get_by_game_id(self, game_id: int):
        query = "SELECT * FROM SumPerPlayer WHERE GameId = ?"
        params = (game_id,)

        r = self._database.execute_query(query, params)
        return self._create_sumperplayer_list(r)

    @staticmethod
    def _create_sumperplayer_list(r):
        return [SumPerPlayer(game_id=row[0], date=row[1], team_name=row[2],
                             player_id=row[3], player_name=row[4], penalty_sum=row[5],
                             full=row[6], clear=row[7], errors=row[8],
                             played=row[9]) for row in r]


class ResultOfGameViewAccess(AbstractDatabaseAccess[ResultOfGame]):
    def get_all(self) -> list[ResultOfGame]:
        r = self._database.execute_query("SELECT * FROM ResultOfGame")
        return [ResultOfGame(id=row[0], totalFull=row[1],
                             totalClear=row[2], totalResult=row[3],
                             totalErrors=row[4]) for row in r]

    def get_by_game_id(self, game_id: int) -> ResultOfGame:
        params = (game_id,)
        r = self._database.execute_single_query("SELECT * FROM ResultOfGame WHERE Id = ?", params)
        return ResultOfGame(id=r[0], totalFull=r[1],
                            totalClear=r[2], totalResult=r[3],
                            totalErrors=r[4])


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
