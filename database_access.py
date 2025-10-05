import abc
from typing import Generic, TypeVar
from entities import (
    DefaultTeamPlayer,
    Game,
    GamePlayers,
    Penalty,
    PlayerPenalties,
    Team,
    TeamPenalties,
    Player,
    Season
)
from database import Database
from view_data_classes import (
    SumPerPlayer,
    ResultOfGame,
    SumPerGame,
    SumPerTeam
)
from collections.abc import Callable

T = TypeVar('T')


class AbstractDatabaseObject(abc.ABC, Generic[T]):    
    def __init__(self, database_connection: Database):
        self._database: Database = database_connection
        self._table_name: str = ""
        self._mapper: Callable[[tuple], T] = None
        
    def _create_select_query(self) -> str:
        return f"SELECT * FROM {self._table_name}"
    
    def get_all(self) -> list[T]:
        rows = self._database.execute_query(self._create_select_query())
        return [self._mapper(row) for row in rows]
    
    def commit(self):
        self._database.commit()
        
    def rollback(self):
        self._database.rollback()


class SeasonTable(AbstractDatabaseObject[Season]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "Seasons"
        self._mapper = lambda row: Season(*row)


class DefaultTeamPlayerTable(AbstractDatabaseObject[DefaultTeamPlayer]):
    def __init__(self, database_connection,):
        super().__init__(database_connection)
        self._table_name = "DefaultTeamPlayer"
        self._mapper = lambda row: DefaultTeamPlayer(*row)


class GameTable(AbstractDatabaseObject[Game]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "Game"
        self._mapper = lambda row: Game(*row)
        
    def insert(self, team_id: int, game_date: str, opponent: str, game_day: int, season_id: int) -> int:
        query = f"""INSERT INTO {self._table_name} 
                   (Team, Date, Vs, GameDay, SeasonId)
                   VALUES (?, ?, ?, ?, ?)"""
        params = (team_id, game_date, opponent, game_day, season_id)
        new_id = self._database.execute_command(query, params)
        return new_id


class GamePlayerTable(AbstractDatabaseObject[GamePlayers]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "GamePlayers"
        self._mapper = lambda row: GamePlayers(*row)

    def insert(self, game_player: GamePlayers) -> int:
        query = f"""INSERT INTO {self._table_name} 
                   (Game, Player, Paid, Result, Full, Clear, Errors, Played)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (
            game_player.game,
            game_player.player,
            game_player.paid,
            game_player.sum_points,
            game_player.full,
            game_player.clear,
            game_player.errors,
            int(game_player.played)
        )
        
        return self._database.execute_command(query, params)

    def get_by_game_and_player(
        self, game_id: int, player_id: int
    ) -> GamePlayers:
        query = self._create_select_query() + " WHERE Game = ? AND Player = ?"
        params = (game_id, player_id)
        r = self._database.execute_single_query(query, params)

        return self._mapper(r)

    def update(self, game_player: GamePlayers) -> None:
        query = f"""UPDATE {self._table_name} 
                   SET Result = ?,
                       Full = ?,
                       Clear = ?,
                       Errors = ?
                   WHERE Id = ?"""

        params = (
            game_player.sum_points,
            game_player.full,
            game_player.clear,
            game_player.errors,
            game_player.id
        )
        self._database.execute_command(query, params)


class PenaltyTable(AbstractDatabaseObject[Penalty]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "Penalty"
        self._mapper = lambda row: Penalty(*row)

    def get_by_id(self, penalty_id: int) -> Penalty:
        query = self._create_select_query() + " WHERE Id = ?"
        params = (penalty_id,)
        r = self._database.execute_single_query(query, params)

        return self._mapper(r)


class PlayerPenaltiesTable(AbstractDatabaseObject[PlayerPenalties]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "PlayerPenalties"
        self._mapper = lambda row: PlayerPenalties(*row)

    def get_by_gameplayerid(self, gameplayerid: int) -> list[PlayerPenalties]:
        query = self._create_select_query() + " WHERE GamePlayer = ?"
        params = (gameplayerid,)
        r = self._database.execute_query(query, params)

        return [self._mapper(row) for row in r]

    def update(self, player_penalty: PlayerPenalties):
        query = """UPDATE PlayerPenalties 
                   SET Value = ?
                   WHERE Id = ?"""

        params = (player_penalty.value, player_penalty.id)
        self._database.execute_command(query, params)
        
    def insert(self, player_penalty: PlayerPenalties) -> int:
        query = """INSERT INTO PlayerPenalties 
                   (GamePlayer, Penalty, Value)
                   VALUES (?, ?, ?)"""
        params = (
            player_penalty.game_player,
            player_penalty.penalty,
            player_penalty.value
        )
        
        return self._database.execute_command(query, params)


class PlayerTable(AbstractDatabaseObject[Player]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "Player"
        self._mapper = lambda row: Player(*row)


class TeamTableAccess(AbstractDatabaseObject[Team]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "Team"
        self._mapper = lambda row: Team(*row)


class TeamPenaltiesTableAccess(AbstractDatabaseObject[TeamPenalties]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "TeamPenalties"
        self._mapper = lambda row: TeamPenalties(*row)


class SumPerTeamViewAccess(AbstractDatabaseObject[SumPerTeam]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "SumPerTeam"
        self._mapper = lambda row: SumPerTeam(*row)


class SumPerPlayerView(AbstractDatabaseObject[SumPerPlayer]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "SumPerPlayer"
        self._mapper = lambda row: SumPerPlayer(*row)

    def get_by_game_id(self, game_id: int):
        query = self._create_select_query() + " WHERE GameId = ?"
        params = (game_id,)

        r = self._database.execute_query(query, params)
        return [self._mapper(row) for row in r]


class ResultOfGameView(AbstractDatabaseObject[ResultOfGame]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "ResultOfGame"
        self._mapper = lambda row: ResultOfGame(*row)

    def get_by_game_id(self, game_id: int) -> ResultOfGame:
        params = (game_id,)
        r = self._database.execute_single_query(
            self._create_select_query() + " WHERE Id = ?", params
        )
        return self._mapper(r)


class SumPerGameView(AbstractDatabaseObject[SumPerGame]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "SumPerGame"
        self._mapper = lambda row: SumPerGame(*row)
    
    def get_by_game_id(self, game_id: int) -> SumPerGame:
        params = (game_id,)
        r = self._database.execute_single_query(
            self._create_select_query() + " WHERE GameId = ?", params
        )
        return self._mapper(r)


if __name__ == "__main__":
    database_access = Database('Kegelkasse.db')
    tableManager = DefaultTeamPlayerTable(database_access)
    result = tableManager.get_all()

    for player in result:
        print(player)

    tableManager = GameTable(database_access)
    result = tableManager.get_all()

    for player in result:
        print(player)
