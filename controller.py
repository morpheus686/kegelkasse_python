from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QDialog

from delegates import PushButtonDelegate
from edit_player_dialog import Ui_Dialog
from main_window import Ui_MainWindow
from model import MainWindowModel, EditPenaltyDialogModel
from table_data_classes import PlayerPenalties
from view_data_classes import SumPerPlayer


class MainWindowController:
    def __init__(self, model: MainWindowModel, view: Ui_MainWindow):
        self.view: Ui_MainWindow = view
        self.model = model
        self.view.pushButton.clicked.connect(lambda: self.pushbutton_clicked())
        self.view.tableView.doubleClicked.connect(lambda: self.table_doubleclick())

    def load_table_view(self):
        table_model = self.model.penalty_table_model
        table_model.insertRows(QModelIndex(), rows=self.model.viewAccess.get_all())
        self.view.tableView.setModel(table_model)
        delegate = PushButtonDelegate(self.view.tableView)
        self.view.tableView.setItemDelegateForColumn(8, delegate)

    def update_view(self):
        all_penalties = self.model.get_all_player_penalties()

    def pushbutton_clicked(self):
        pass

    def table_doubleclick(self):
        selection_model = self.view.tableView.selectionModel()
        current_index = selection_model.currentIndex()
        selected_player = self.model.penalty_table_model.get(current_index.row())

        game_player = self.model.game_player_access.get_by_game_and_player(selected_player.game_id,
                                                                           selected_player.player_id)

        dialog_model = EditPenaltyDialogModel(selected_player, game_player)

        dialog = QDialog()
        edit_players_penalties_dialog = Ui_Dialog()
        edit_players_penalties_dialog.setupUi(dialog)

        dialog_controller = EditPenaltyDialogController(dialog_model,
                                                        edit_players_penalties_dialog)
        dialog_controller.load_dialog()

        dialog.exec()
        dialog_result = dialog.result()
        print(dialog_result)

        if dialog_result:
            pass


class EditPenaltyDialogController:
    def __init__(self, edit_player_penalties_model: EditPenaltyDialogModel,
                 edit_player_penalty_view: Ui_Dialog) -> None:
        self._edit_player_penalties_model = edit_player_penalties_model
        self._edit_player_penalty_view = edit_player_penalty_view

    def load_dialog(self):
        pass



