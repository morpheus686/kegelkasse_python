from typing import Any, Union, TypeVar, Generic
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    QAbstractListModel
)
from PySide6.QtGui import Qt
from database import Database
from database_access import (
    SumPerPlayerView,
    GamePlayerTable,
    PlayerPenaltiesTable,
    PenaltyTable,
    GameTable,
    ResultOfGameView,
    SumPerGameView,
    PlayerTable,
    SeasonTable
)
from entities import PlayerPenalties, GamePlayers, Season
from view_data_classes import SumPerPlayer
from dataclasses import dataclass
from datetime import date
from abc import abstractmethod


class MainWindowModel:
    def __init__(self, db_name: str):
        self._database = Database(db_name)
        self._sum_per_player_view = SumPerPlayerView(
            self._database
        )
        
        self._game_player_table = GamePlayerTable(self._database)
        self._player_penalty_table = PlayerPenaltiesTable(
            self._database
        )
        self._penalty_table = PenaltyTable(self._database)
        self._game_table = GameTable(self._database)
        
        self._result_of_game_view = ResultOfGameView(self._database)
        self._sum_per_game_view = SumPerGameView(self._database)
    
    def get_all_games(self):
        return self._game_table.get_all()

    def get_results_per_game(self, game_id: int):
        return self._result_of_game_view.get_by_game_id(game_id)
    
    def get_all_sum_per_player(self, game_id: int) -> list[SumPerPlayer]:
        return self._sum_per_player_view.get_by_game_id(game_id)
        
    def get_by_game_and_player_id(
        self,
        game_id: int,
        player_id: int
    ) -> Union[GamePlayers, None]:
        return self._game_player_table.get_by_game_and_player(
            game_id,
            player_id
        )
        
    def get_sum_per_game(self, game_id: int):
        return self._sum_per_game_view.get_by_game_id(game_id)
        
    def get_penalty(self, penalty_id: int):
        return self._penalty_table.get_by_id(penalty_id)
    
    def get_penalty_by_gameplayerid(
                                    self, game_player_id: int
            ) -> list[PlayerPenalties]:
        return self._player_penalty_table.get_by_gameplayerid(game_player_id)
        
    def update_game_player(self, game_player: GamePlayers):
        self._game_player_table.update(game_player)
        
    def update_player_penalty(self, player_penalty: PlayerPenalties):
        self._player_penalty_table.update(player_penalty)
        
    def update_game_player_with_penalties(
        self,
        game_player: GamePlayers,
        player_penalties: list[PlayerPenalties]
    ):
        with self._database.transaction():
            self.update_game_player(game_player)
            
            for pp in player_penalties:
                self.update_player_penalty(pp)


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


class AddGameDialogModel:
    def __init__(self, database):
        self._database = database
        self.game_date = date.today()
        self.opponent = ""
        self.game_day = 1
        self.selected_season = 0
        
        self._players = []
        self._seasons = []
        
    @property
    def players(self):
        return self._players
    
    @property
    def seasons(self):
        return self._seasons
    
    def load(self) -> None:
        player_table = PlayerTable(self._database)
        all_players = player_table.get_all()
        self._players = [PlayerTableModelItem(False, p.name, p.id) for p in all_players]
        
        season_table = SeasonTable(self._database)
        self._seasons = season_table.get_all()
        
    def save_game(self):
        with self._database.transaction():
            game_table = GameTable(self._database)
            new_game_id = game_table.insert(
                1,
                self.game_date,
                self.opponent,
                self.game_day,
                self.selected_season)

            game_players = [GamePlayers(
                None,
                new_game_id,
                p.player_id,
                0,
                0,
                0,
                0,
                0,
                True,
                None)
                for p in self._players if p.is_playing]
            
            game_player_table = GamePlayerTable(self._database)
            game_player_ids = [game_player_table.insert(gp) for gp in game_players]
            
            penalty_table = PenaltyTable(self._database)
            penalty_ids = [penalty.id for penalty in penalty_table.get_all()]
            player_penalty_table = PlayerPenaltiesTable(self._database)
            
            for game_player_id in game_player_ids:
                player_penalties = [PlayerPenalties(
                    None,
                    game_player_id,
                    pid,
                    0,
                    None)
                    for pid in penalty_ids]                
  
                [player_penalty_table.insert(pp) for pp in player_penalties]


T = TypeVar('T')


class ListModel(QAbstractListModel, Generic[T]):
    def __init__(self, items=None, parent=...):
        super().__init__(parent)
        self._items: list[T] = items or []
        
    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return None
        
        item = self._items[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self.get_label(item)
        elif role == Qt.ItemDataRole.UserRole:
            return self.get_id(item)
        
        return None
        
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._items)
    
    @abstractmethod
    def get_label(self, item: T) -> str:
        pass
    
    @abstractmethod
    def get_id(self, item: T) -> int:
        pass


class SeasonListModel(ListModel[Season]):
    def __init__(self, items: list[Season] = None, parent=None):
        super().__init__(items, parent)
    
    def get_label(self, item: Season) -> str:
        return item.name
    
    def get_id(self, item: Season) -> int:
        return item.id


class AbstractTableModel(QAbstractTableModel, Generic[T]):
    def __init__(self):
        super().__init__()
        self._source: list[T] = []

    def get(self, index: int) -> T:
        return self._source[index]

    def insertRows(self, index, rows, parent=...):
        if not rows:
            return False

        position = index.row()

        self.beginInsertRows(parent, position, position + len(rows) - 1)
        self._source[position:position] = rows
        self.endInsertRows()

        return True

    def removeRows(self, row, count, parent=...):
        if row < 0 or count <= 0 or row >= len(self._source):
            return False

        end_row = min(row + count - 1, len(self._source) - 1)
        self.beginRemoveRows(QModelIndex(), row, end_row)

        del self._source[row:end_row + 1]

        self.endRemoveRows()

    def remove_all_rows(self):
        if self._source:
            self.removeRows(0, len(self._source), QModelIndex())

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._source)
  

class SumPerPlayerTablemodel(AbstractTableModel[SumPerPlayer]):
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
            return Qt.CheckState.Checked if True else Qt.CheckState.Unchecked

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


class PlayerPenaltiesTableModel(AbstractTableModel[PlayerPenalties]):
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
        for index, row in enumerate(self._source):
            if row.penalty_navigation.get_value_by_parent:
                return index

        return -1


@dataclass
class PlayerTableModelItem():
    is_playing: bool
    player_name: str
    player_id: int


class PlayerTableModel(AbstractTableModel[PlayerTableModelItem]):
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
                        return ""
                    case 1:
                        return "Spieler"
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

        return None

    def columnCount(self, parent=...):
        return 2
    
    def data(
        self,
        index: Union[QModelIndex, QPersistentModelIndex],
        role: int = ...
    ) -> Any:
        row = self._source[index.row()]
        column_index = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column_index == 1:
                return row.player_name
        
        if (
            role == Qt.ItemDataRole.CheckStateRole
            and column_index == 0
        ):
            return Qt.CheckState.Checked if row.is_playing else Qt.CheckState.Unchecked

        return None
    
    def setData(self, index, value, role=...):
        if not index.isValid() or index.column() != 0:
            return False
        
        if role in [Qt.ItemDataRole.CheckStateRole, Qt.ItemDataRole.DisplayRole]:
            row = self._source[index.row()]
            row.is_playing = (value == Qt.CheckState.Checked.value)
            self.dataChanged.emit(index, index, [role])
            return True
        
        return False
    
    def flags(self, index: QModelIndex):
        flags = super().flags(index)
        
        if index.column() == 0:
            flags = flags | Qt.ItemFlag.ItemIsUserCheckable

        return flags
    
    @property
    def is_any_player_selected(self) -> bool:
        return any(item.is_playing for item in self._source)
