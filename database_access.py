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
    Player
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
    def __init__(
            self, database_connection: Database):
        self._database: Database = database_connection
        self._table_name: str = ""
        self._mapper: Callable[[tuple], T] = None
        
    def _create_select_query(self) -> str:
        return f"SELECT * FROM {self._table_name}"
    
    def get_all(self) -> list[T]:
        rows = self._database.execute_query(self._create_select_query())
        return [self._mapper(row) for row in rows]

    async def get_all_async(self) -> list[T]:
        rows = await self._database.execute_query_async(
            self._create_select_query())
        return [self._mapper(row) for row in rows]


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


class GamePlayerTable(AbstractDatabaseObject[GamePlayers]):
    def __init__(self, database_connection):
        super().__init__(database_connection)
        self._table_name = "GamePlayers"
        self._mapper = lambda row: GamePlayers(*row)

    def get_by_game_and_player(
        self, game_id: int, player_id: int
    ) -> GamePlayers:
        query = self._create_select_query() + " WHERE Game = ? AND Player = ?"
        params = (game_id, player_id)
        r = self._database.execute_single_query(query, params)

        return self._mapper(r)
        
    async def get_by_game_and_player_async(
        self, game_id: int, player_id: int
    ) -> GamePlayers:
        query = self._create_select_query() + " WHERE Game = ? AND Player = ?"
        params = (game_id, player_id)
        r = await self._database.execute_single_query_async(query, params)

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
        
    async def update_async(self, game_player: GamePlayers) -> None:
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
        await self._database.execute_command_async(query, params)


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
        
    async def get_by_id_async(self, penalty_id: int) -> Penalty:
        query = "SELECT * FROM Penalty WHERE Id = ?"
        params = (penalty_id,)
        r = await self._database.execute_single_query_async(query, params)

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

    async def get_by_gameplayerid_async(
                                        self, gameplayerid: int
            ) -> list[PlayerPenalties]:
        query = self._create_select_query() + " WHERE GamePlayer = ?"
        params = (gameplayerid,)
        r = await self._database.execute_query_async(query, params)

        return [self._mapper(row) for row in r]

    def update(self, player_penalty: PlayerPenalties):
        query = """UPDATE PlayerPenalties 
                   SET Value = ?
                   WHERE Id = ?"""

        params = (player_penalty.value, player_penalty.id)
        self._database.execute_command(query, params)
        
    async def update_async(self, player_penalty: PlayerPenalties):
        query = """UPDATE PlayerPenalties 
                   SET Value = ?
                   WHERE Id = ?"""

        params = (player_penalty.value, player_penalty.id)
        await self._database.execute_command_async(query, params)


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
    
    async def get_by_game_id_async(self, game_id: int):
        query = self._create_select_query() + " WHERE GameId = ?"
        params = (game_id,)

        r = await self._database.execute_query_async(query, params)
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
        
    async def get_by_game_id_async(
        self, game_id: int
    ) -> ResultOfGame:
        params = (game_id,)
        r = await self._database.execute_single_query_async(
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
    
    async def get_by_game_id_async(self, game_id: int) -> SumPerGame:
        params = (game_id,)
        r = await self._database.execute_single_query_async(
            self._create_select_query() + " WHERE GameId = ?", params
        )
        return self._mapper(r)
    
    async def get_all_async(self) -> list[SumPerGame]:
        pass


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
