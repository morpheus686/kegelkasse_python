from typing import Any, Union, TypeVar, Generic
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import Qt
from database import Database
from database_access import SumPerPlayerViewAccess, GamePlayerTableAccess, PlayerPenaltiesTableAccess, \
    PenaltyTableAccess, GameTableAccess
from table_data_classes import PlayerPenalties, GamePlayers
from view_data_classes import SumPerPlayer


class MainWindowModel:
    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.sum_per_player_view_access = SumPerPlayerViewAccess(self.database)
        self.game_player_access = GamePlayerTableAccess(self.database)
        self.player_penalty_access = PlayerPenaltiesTableAccess(self.database)
        self.penalty_access = PenaltyTableAccess(self.database)
        self.game_access = GameTableAccess(self.database)
        self._penaltyTableModel = SumPerPlayerTablemodel()

    @property
    def penalty_table_model(self):
        return self._penaltyTableModel


class EditPenaltyDialogModel:
    def __init__(self, selected_player: SumPerPlayer, game_player: GamePlayers):
        self.selected_player = selected_player
        self.game_player = game_player


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
    def columnCount(self, parent=QModelIndex()) -> int:
        return 7

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
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
                    return ""
                case 6:
                    return f"{player.penalty_sum:.2f} €"
        elif role == Qt.ItemDataRole.CheckStateRole and index.column() == 5:
            return bool(player.played)

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
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

        if index.column() == 5:
            flags = flags | Qt.ItemFlag.ItemIsUserCheckable

        return flags


class PlayerPenaltiesTableModel(TableModel[PlayerPenalties]):
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

        if role == Qt.ItemDataRole.EditRole and index.column() == 1:
            self._source[index_row].value = new_value
        elif role == Qt.ItemDataRole.DisplayRole:
            new_value = int(value)
            self._source[index_row].value = new_value

        return True

    def flags(self, index):
        flags = super().flags(index)

        if index.column() == 1:
            current_row = self._source[index.row()]

            if not current_row.penalty_navigation.get_value_by_parent:
                flags = flags | Qt.ItemFlag.ItemIsEditable

        return flags

    def get_rowindex_of_error_row(self) -> int:
        row_index = 0

        for row in self._source:
            if row.penalty_navigation.get_value_by_parent:
                return row_index

            row_index += 1

        return -1
