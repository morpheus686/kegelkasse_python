from typing import Union, Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import Qt
from database import Database
from database_access import SumPerPlayerViewAccess


class MainWindowModel:
    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.viewAccess = SumPerPlayerViewAccess(self.database)
        self._penaltyTableModel = PenaltyTableModel(self.viewAccess)

    @property
    def get_penalty_table_model(self):
        return self._penaltyTableModel

    def get_all_player_penalties(self):
        self._penaltyTableModel.load()
        return self.viewAccess.get_all_tuples()


class PenaltyTableModel(QAbstractTableModel):
    def __init__(self, sum_per_player_db_access: SumPerPlayerViewAccess):
        super().__init__()
        self._sum_per_player_db_access = sum_per_player_db_access
        self._players: list[tuple] = []

    def load(self):
        self._players = self._sum_per_player_db_access.get_all_tuples()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._players)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._players[0])

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int) -> Any:
        player = self._players[index.row()]
        column_index = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column_index == 3:
                return f"{player[column_index]:.2f} €"
            else:
                return player[column_index]

        return "Leer"

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> Any:
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                match section:
                    case 0:
                        return "Datum"
                    case 1:
                        return "Spielername"
                    case 2:
                        return "Mannschaft"
                    case 3:
                        return "Strafe"
        elif orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return section + 1

        return None
