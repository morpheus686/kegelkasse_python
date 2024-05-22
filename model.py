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
        return self.viewAccess.get_all()


class PenaltyTableModel(QAbstractTableModel):
    def __init__(self, sum_per_player_db_access: SumPerPlayerViewAccess):
        super().__init__()
        self._sum_per_player_db_access = sum_per_player_db_access
        self._players = []

    def load(self):
        self._players = self._sum_per_player_db_access.get_all()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._players)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 4

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int) -> Any:
        player = self._players[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return player.date
            elif index.column() == 1:
                return player.player_name
            elif index.column() == 2:
                return player.team
            elif index.column() == 3:
                return f"{player.penalty:.2f} €"

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
