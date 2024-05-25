from typing import Any, Union, TypeVar, Generic
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import Qt
from database import Database
from database_access import SumPerPlayerViewAccess, GamePlayerTableAccess
from table_data_classes import PlayerPenalties, GamePlayers
from view_data_classes import SumPerPlayer


class MainWindowModel:
    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.viewAccess = SumPerPlayerViewAccess(self.database)
        self.game_player_access = GamePlayerTableAccess(self.database)
        self._penaltyTableModel = SumPerPlayerTablemodel()

    @property
    def penalty_table_model(self):
        return self._penaltyTableModel

    def get_all_player_penalties(self):
        return self.viewAccess.get_all_tuples()


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

    def _insert_rows_internal(self, index, rows):
        list_len = len(self._source)
        row_count = len(rows)
        end_row = list_len + row_count - 1
        self.beginInsertRows(index, list_len, end_row)

        for row in rows:
            self._source.append(row)

        self.endInsertRows()

    def _remove_rows_internal(self, row, count):
        end_row = row + count - 1
        self.beginRemoveRows(QModelIndex(), row, end_row)

        while end_row >= row:
            if len(self._source) == 0:
                break

            self._source.pop(end_row)
            end_row -= 1

        self.endRemoveRows()

    def remove_all_rows(self):
        self.removeRows(0, len(self._source), QModelIndex())


class SumPerPlayerTablemodel(TableModel[SumPerPlayer]):
    BUTTON_COLUMN_NUMBER = 8

    def __init__(self):
        super().__init__()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._source)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 9

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        player = self._source[index.row()]
        column_index = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            match column_index:
                case 0:
                    return player.date
                case 1:
                    return player.team_name
                case 2:
                    return player.player_name
                case 3:
                    return player.full
                case 4:
                    return player.clear
                case 5:
                    return player.errors
                case 6:
                    return player.played
                case 7:
                    return f"{player.penalty_sum:.2f} €"
                case BUTTON_COLUMN_NUMBER:
                    return "Bearbeiten"

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                match section:
                    case 0:
                        return "Spieldatum"
                    case 1:
                        return "Mannschaft"
                    case 2:
                        return "Spieler"
                    case 3:
                        return "Volle"
                    case 4:
                        return "Abräumen"
                    case 5:
                        return "Fehler"
                    case 6:
                        return "Gespielt"
                    case 7:
                        return "Strafe"
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

        return None

    def removeRows(self, row, count, parent=...):
        self._remove_rows_internal(row, count)

    def insertRows(self, index, rows, parent=...):
        self._insert_rows_internal(index, rows)


class PlayerPenaltiesTableModel(TableModel[PlayerPenalties]):
    def __init__(self, penalties: list[PlayerPenalties]):
        super().__init__()

    def insertRows(self, index, rows, parent=...):
        self._insert_rows_internal(index, rows)

    def removeRows(self, row, count, parent=...):
        self._remove_rows_internal(row, count)
