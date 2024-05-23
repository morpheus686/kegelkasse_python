from PySide6.QtCore import QModelIndex

from delegates import PushButtonDelegate
from main_window import Ui_MainWindow
from model import MainWindowModel


class MainWindowController:
    def __init__(self, model: MainWindowModel, view: Ui_MainWindow):
        self.view: Ui_MainWindow = view
        self.model = model
        self.view.pushButton.clicked.connect(lambda: self.pushbutton_clicked())

    def load_table_view(self):
        table_model = self.model.get_penalty_table_model
        table_model.insertRows(QModelIndex(), rows=self.model.viewAccess.get_all())
        self.view.tableView.setModel(table_model)
        delegate = PushButtonDelegate(self.view.tableView)
        self.view.tableView.setItemDelegateForColumn(8, delegate)

    def update_view(self):
        all_penalties = self.model.get_all_player_penalties()

    def pushbutton_clicked(self):
        pass

