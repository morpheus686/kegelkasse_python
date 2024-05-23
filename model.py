from typing import Any, Union
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import Qt
from database import Database
from database_access import SumPerPlayerViewAccess
from view_data_classes import SumPerPlayer


class MainWindowModel:
    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.viewAccess = SumPerPlayerViewAccess(self.database)
        self._penaltyTableModel = PenaltyTableModel(self.viewAccess)

    @property
    def get_penalty_table_model(self):
        return self._penaltyTableModel

    def get_all_player_penalties(self):
        return self.viewAccess.get_all_tuples()


class PenaltyTableModel(QAbstractTableModel):
    BUTTON_COLUMN_NUMBER = 8

    def __init__(self, sum_per_player_db_access: SumPerPlayerViewAccess):
        super().__init__()
        self._sum_per_player_db_access = sum_per_player_db_access
        self._players: list[SumPerPlayer] = []

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._players)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 9

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:
        player = self._players[index.row()]
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
        end_row = row + count - 1
        self.beginRemoveRows(QModelIndex(), row, end_row)

        while end_row >= row:
            if len(self._players) == 0:
                break

            self._players.pop(end_row)
            end_row -= 1

        self.endRemoveRows()

    def insertRows(self, index, rows, parent=...):
        list_len = len(self._players)
        row_count = len(rows)
        end_row = list_len + row_count - 1
        self.beginInsertRows(index, list_len, end_row)

        for row in rows:
            self._players.append(row)

        self.endInsertRows()

    def remove_all_rows(self):
        self.removeRows(0, len(self._players), QModelIndex())
