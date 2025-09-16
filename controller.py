from PySide6.QtCore import QModelIndex, Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QDialog
from delegates import SpinBoxDelegate
from edit_player_dialog import Ui_Dialog
from ui_maindow import Ui_MainWindow
from model import (
    MainWindowModel,
    EditPenaltyDialogModel,
    PlayerPenaltiesTableModel,
    SumPerPlayerTablemodel,
)
from entities import Game
import asyncio
import abc


class MainWindowController:
    def __init__(self, model: MainWindowModel, mainWindow) -> None:
        self._window = mainWindow
        self._view: Ui_MainWindow = mainWindow.ui
        self._model = model
        self._currentGame: Game | None = None
        self._games: list[Game] = []
        self._penalty_tablemodel = SumPerPlayerTablemodel()
        self._sort_proxy_model = QSortFilterProxyModel()
        self._loop = asyncio.get_event_loop()
        
        self._window.loaded.connect(self.window_loaded)
        self._view.previous_push_button.clicked.connect(
            self.previous_button_clicked
            )
        self._view.next_push_button.clicked.connect(
            self.next_pushbutton_clicked
            )
        self._view.tableView.doubleClicked.connect(self.table_doubleclick)
        
    def window_loaded(self):
        self.initialize()
        
    async def initialize_async(self) -> None:
        self._games = await self._model.game_access.get_all_async()
        
        if self._games:
            self._sort_proxy_model.setSourceModel(self._penalty_tablemodel)
            self._currentGame = self._games[-1]
            self._view.tableView.setModel(self._sort_proxy_model)
            
            self.set_current_game_label()
            self.set_enabled_of_previous_pushbutton()
            self.set_enabled_of_next_pushbutton()

    def initialize(self) -> None:
        self._games = self._model.get_all_games()
        
        if self._games:
            self._sort_proxy_model.setSourceModel(self._penalty_tablemodel)
            self._currentGame = self._games[-1]
            self.fill_form()
            self._view.tableView.setModel(self._sort_proxy_model)
            
            self.set_current_game_label()
            self.set_enabled_of_previous_pushbutton()
            self.set_enabled_of_next_pushbutton()

    def set_current_game_label(self):
        self._view.game_day_label.setText(self._currentGame.date)

    def fill_form(self):
        self._update_table_in_view()
        self.update_game_stats_in_view()
        self._update_sum_in_view()
        
    def _update_table_in_view(self):
        table_model = self._penalty_tablemodel
        table_model.remove_all_rows()
        
        sum_per_players = self._model.get_all_sum_per_player(
            self._currentGame.id
        )
        insert_index = table_model.createIndex(0, 0, QModelIndex())
        table_model.insertRows(
            insert_index,
            rows=sum_per_players,
            parent=QModelIndex()
        )
        
        self._view.tableView.resizeColumnsToContents()

    def update_game_stats_in_view(self):
        game_stats = self._model.get_results_per_game(
            self._currentGame.id
        )
        
        self._view.teamresult_lineedit.setText(str(game_stats.totalResult))
        self._view.teamerrors_lineEdit.setText(str(game_stats.totalErrors))
        self._view.full_lineEdit.setText(str(game_stats.totalFull))
        self._view.clear_lineEdit.setText(str(game_stats.totalClear))

    def _update_sum_in_view(self):
        sum_of_game = self._model.get_sum_per_game(
            self._currentGame.id
            )
        
        self._view.paysum_lineedit.setText(f"{sum_of_game.penalty_sum:.2f} €")

    async def fill_form_async(self):
        table_model = self._penalty_tablemodel
        table_model.remove_all_rows()
        sum_per_players = await self._model.get_all_sum_per_player_async(
                self._currentGame.id
            )
        insert_index = table_model.createIndex(0, 0, QModelIndex())
        table_model.insertRows(
            insert_index, 
            rows=sum_per_players, 
            parent=QModelIndex()
            )

        game_stats = await self._model.get_results_per_game_async(
            self._currentGame.id
            )
        self._view.teamresult_lineedit.setText(str(game_stats.totalResult))
        self._view.teamerrors_lineEdit.setText(str(game_stats.totalErrors))
        self._view.full_lineEdit.setText(str(game_stats.totalFull))
        self._view.clear_lineEdit.setText(str(game_stats.totalClear))
        self._view.tableView.resizeColumnsToContents()

        sum_of_game = await self._model.get_sum_per_game_async(
            self._currentGame.id
            )
        self._view.paysum_lineedit.setText(f"{sum_of_game.penalty_sum:.2f} €")

    def previous_button_clicked(self):
        current_index = self.get_current_index_of_game()
        previous_index = current_index - 1
        self._currentGame = self._games[previous_index]
        self.set_current_game_label()
        self.fill_form()

        self.set_enabled_of_previous_pushbutton()
        self.set_enabled_of_next_pushbutton()

    def set_enabled_of_previous_pushbutton(self):
        at_first_index = self.get_current_index_of_game() == 0
        self._view.previous_push_button.setEnabled(not at_first_index)

    def next_pushbutton_clicked(self):
        current_index = self.get_current_index_of_game()
        next_index = current_index + 1
        self._currentGame = self._games[next_index]
        self.set_current_game_label()
        self.fill_form()

        self.set_enabled_of_next_pushbutton()
        self.set_enabled_of_previous_pushbutton()

    def set_enabled_of_next_pushbutton(self):
        last_index = len(self._games) - 1
        at_last_index = self.get_current_index_of_game() == last_index
        self._view.next_push_button.setEnabled(not at_last_index)

    def get_current_index_of_game(self):
        current_index = self._games.index(self._currentGame)
        return current_index

    def table_doubleclick(self):
        selection_model = self._view.tableView.selectionModel()
        current_index = selection_model.currentIndex()
        selected_player = self._penalty_tablemodel.get(current_index.row())

        game_player = self._model.get_by_game_and_player_id(
            selected_player.game_id,
            selected_player.player_id
            )
        player_penalties = self._model.get_penalty_by_gameplayerid(
            game_player.id
            )

        for player_penalty in player_penalties:
            player_penalty.penalty_navigation = self._model.get_penalty(
                player_penalty.penalty
                )

        game_player.player_penalties_navigation = player_penalties
        dialog_model = EditPenaltyDialogModel(selected_player, game_player)

        dialog_controller = EditPenaltyDialogController(
            dialog_model, Ui_Dialog()
        )
        dialog_result = dialog_controller.show_dialog()

        if dialog_result:
            self._model.update_game_player(game_player)

            for player_penalty in player_penalties:
                self._model.update_player_penalty(player_penalty)

            self.fill_form()


class DialogController(abc.ABC):
    def __init__(self, model, view):
        self._model = model
        self._dialog = QDialog()
        self._view = view
        
        self._view.setupUi(self._dialog)
    
    @abc.abstractmethod
    def show_dialog(self) -> int:
        pass
    
    @property
    def model(self):
        return self._model


class EditPenaltyDialogController(DialogController):
    def __init__(
            self,
            edit_player_penalties_model: EditPenaltyDialogModel,
            view) -> None:
        super().__init__(edit_player_penalties_model, view)
             
        self._table_model = PlayerPenaltiesTableModel()
        
        self._view.full_spin_box.setValue(self._model.game_player.full)
        self._view.clear_spin_box.setValue(self._model.game_player.clear)
        self._view.error_spin_box.setValue(self._model.game_player.errors)
        
        self._view.full_spin_box.valueChanged.connect(
            self.__full_value_changed
        )
        self._view.clear_spin_box.valueChanged.connect(
            self.__clear_value_changed
        )
        self._view.error_spin_box.valueChanged.connect(
            self.__error_value_changed
            )
        
    def show_dialog(self) -> int:
        self.__initialize()
        self._dialog.exec()
        return self._dialog.result()

    def __initialize(self):
        insert_index = self._table_model.createIndex(0, 0, QModelIndex())
        self._table_model.insertRows(
            insert_index,
            self._model.game_player.player_penalties_navigation,
            QModelIndex()
        )

        self._view.penaltyTable.setItemDelegate(SpinBoxDelegate())
        self._view.penaltyTable.setModel(self._table_model)

        self.__set_total_line_edit()

    def __full_value_changed(self):
        self.__set_total_line_edit()
        self._model.game_player.full = self._view.full_spin_box.value()

    def __clear_value_changed(self):
        self.__set_total_line_edit()
        self._model.game_player.clear = self._view.clear_spin_box.value()

    def __set_total_line_edit(self):
        full = self._view.full_spin_box.value()
        clear = self._view.clear_spin_box.value()
        total = full + clear
        
        self._view.total_line_edit.setText(str(total))

    def __error_value_changed(self):
        self._model.game_player.errors = self._view.error_spin_box.value()
        error_row_index = self._table_model.get_rowindex_of_error_row()
        index = self._table_model.index(error_row_index, 1, QModelIndex())
        self._table_model.setData(index, self._view.error_spin_box.value(),
                                  Qt.ItemDataRole.DisplayRole)
