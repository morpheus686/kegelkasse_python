from typing import Any, Union, TypeVar, Generic
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
)
from PySide6.QtGui import Qt
from database import Database
from database_access import (
    SumPerPlayerViewAccess,
    GamePlayerTableAccess,
    PlayerPenaltiesTableAccess,
    PenaltyTableAccess,
    GameTableAccess,
    ResultOfGameViewAccess,
    SumPerGameViewAccess,
)
from table_data_classes import PlayerPenalties, GamePlayers
from view_data_classes import SumPerPlayer


class MainWindowModel:
    def __init__(self, db_name: str):
        self._database = Database(db_name)
        self._sum_per_player_view_access = SumPerPlayerViewAccess(
            self._database
        )
        self._sum_per_game_view_access = SumPerGameViewAccess(self._database)
        self._game_player_access = GamePlayerTableAccess(self._database)
        self._player_penalty_access = PlayerPenaltiesTableAccess(
            self._database
        )
        self._penalty_access = PenaltyTableAccess(self._database)
        self._game_access = GameTableAccess(self._database)
        self._result_of_game_access = ResultOfGameViewAccess(self._database)
    
    def get_all_games(self):
        return self._game_access.get_all()
    
    async def get_all_games_async(self):
        return await self._game_access.get_all_async()

    def get_results_per_game(self, game_id: int):
        return self._result_of_game_access.get_by_game_id(game_id)
    
    async def get_results_per_game_async(self, game_id: int):
        return await self._result_of_game_access.get_by_game_id_async(
            game_id
        )
    
    def get_all_sum_per_player(self, game_id: int) -> list[SumPerPlayer]:
        return self._sum_per_player_view_access.get_by_game_id(game_id)
    
    async def get_all_sum_per_player_async(self, game_id: int) -> list[SumPerPlayer]:
        return await self._sum_per_player_view_access.get_by_game_id_async(
            game_id
        )
        
    def get_by_game_and_player_id(
        self,
        game_id: int,
        player_id: int
    ) -> Union[GamePlayers, None]:
        return self._game_player_access.get_by_game_and_player(
            game_id,
            player_id
        )
        
    async def get_by_game_and_player_id_async(
        self,
        game_id: int,
        player_id: int
    ) -> Union[GamePlayers, None]:
        return await self._game_player_access.get_by_game_and_player_id_async(
            game_id,
            player_id
        )
        
    def get_sum_per_game(self, game_id: int):
        return self._sum_per_game_view_access.get_by_game_id(game_id)
    
    async def get_sum_per_game_async(self, game_id: int):
        return await self._sum_per_game_view_access.get_by_game_id_async(
            game_id
        )
        
    def get_penalty(self, penalty_id: int):
        return self._penalty_access.get_by_id(penalty_id)
    
    async def get_penalty_async(self, penalty_id: int):
        return await self._penalty_access.get_by_id_async(penalty_id)
    
    def get_penalty_by_gameplayerid(self, game_player_id: int) -> list[PlayerPenalties]:
        return self._player_penalty_access.get_by_gameplayerid(game_player_id)
    
    async def get_penalty_by_gameplayerid_async(self, game_player_id: int) -> list[PlayerPenalties]:
        return await self._player_penalty_access.get_by_gameplayerid_async(
            game_player_id
        )
        
    def update_game_player(self, game_player: GamePlayers):
        self._game_player_access.update(game_player)
        
    async def update_game_player_async(self, game_player: GamePlayers):
        await self._game_player_access.update_async(game_player)
        
    def update_player_penalty(self, player_penalty: PlayerPenalties):
        self._player_penalty_access.update(player_penalty)

    async def update_player_penalty_async(self, player_penalty: PlayerPenalties):
        await self._player_penalty_access.update_async(player_penalty)
    
    
class EditPenaltyDialogModel:
    def __init__(
        self,
        selected_player: SumPerPlayer,
        game_player: GamePlayers
    ):
        self._selected_player = selected_player
        self._game_player = game_player

    @property
    def game_player(self):
        return self._game_player

    @property
    def selected_player(self):
        return self._selected_player


T = TypeVar('T')


class TableModel(QAbstractTableModel, Generic[T]):
    def __init__(self):
        super().__init__()
        self._source: list[T] = []
       
    def get(self, index: int) -> T:
        return self._source[index]

    def insertRows(self, index, rows, parent=...):
        position = index.row()
        self.beginInsertRows(parent, position, position + len(rows) - 1)

        for row in rows:
            self._source.insert(position, row)
            position += 1

        self.endInsertRows()
        return True

    def removeRows(self, row, count, parent=...):
        end_row = row + count - 1
        self.beginRemoveRows(QModelIndex(), row, end_row)

        while end_row >= row:
            if len(self._source) == 0:
                break

            self._source.pop(end_row)
            end_row -= 1

        self.endRemoveRows()

    def remove_all_rows(self):
        if self._source:
            self.removeRows(0, len(self._source), QModelIndex())

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._source)


class SumPerPlayerTablemodel(TableModel[SumPerPlayer]):
    PLAYED_COLUMN_INDEX = 5

    def columnCount(self, parent=QModelIndex()) -> int:
        return 7

    def data(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        role: int = ...
    ) -> Any:
        player = self._source[index.row()]
        column_index = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            match column_index:
                case 0:
                    return player.player_name
                case 1:
                    return player.full
                case 2:
                    return player.clear
                case 3:
                    return player.full + player.clear
                case 4:
                    return player.errors
                case 5:
                    return None
                case 6:
                    return (
                        f"{player.penalty_sum:.2f} €"
                    )
        if (
            role == Qt.ItemDataRole.CheckStateRole
            and index.column() == self.PLAYED_COLUMN_INDEX
        ):
            return bool(player.played)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = ...
    ) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                match section:
                    case 0:
                        return "Spieler"
                    case 1:
                        return "Volle"
                    case 2:
                        return "Abräumen"
                    case 3:
                        return "Gesamt"
                    case 4:
                        return "Fehler"
                    case 5:
                        return "Gespielt"
                    case 6:
                        return "Strafe"
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

        return None

    def flags(self, index):
        flags = super().flags(index)

        if index.column() == self.PLAYED_COLUMN_INDEX:
            flags = flags | Qt.ItemFlag.ItemIsUserCheckable

        return flags


class PlayerPenaltiesTableModel(TableModel[PlayerPenalties]):
    EDITABLE_COLUMN = 1

    def columnCount(self, parent=...):
        return 3

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                match section:
                    case 0:
                        return "Regel"
                    case 1:
                        return "Anzahl"
                    case 2:
                        return "Summe"
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

    def data(self, index, role=...):
        row = self._source[index.row()]
        column_index = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            match column_index:
                case 0:
                    return row.penalty_navigation.description
                case 1:
                    return row.value
                case 2:
                    total = row.value * row.penalty_navigation.penalty
                    return f"{total:.2f} €"

        return None

    def setData(self, index, value, role=...):
        new_value = int(value)
        index_row = index.row()
        index_column = index.column()

        if index_column == self.EDITABLE_COLUMN:
            if role in [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]:
                self._source[index_row].value = new_value
                roles = [role]
                self.dataChanged.emit(index, index, roles)
                pay_index = self.index(
                    index_row, index_column + 1, QModelIndex()
                )
                self.dataChanged.emit(pay_index, pay_index, roles)

        return True

    def flags(self, index):
        flags = super().flags(index)

        if index.column() == self.EDITABLE_COLUMN:
            current_row = self._source[index.row()]

            if not current_row.penalty_navigation.get_value_by_parent:
                flags = flags | Qt.ItemFlag.ItemIsEditable

        return flags

    def get_rowindex_of_error_row(self) -> int:
        row_index: int = 0

        for row in self._source:
            if row.penalty_navigation.get_value_by_parent:
                return row_index

            row_index += 1

        return -1
