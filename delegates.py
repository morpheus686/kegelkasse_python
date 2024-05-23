from PySide6.QtWidgets import QItemDelegate, QPushButton, QTableView, QWidget, QStyledItemDelegate


class PushButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QTableView, option, index) -> QWidget:
        push_button = QPushButton(text="Bearbeiten", parent=parent)
        push_button.clicked.connect(lambda ix=index: self.button_clicked(ix))
        return push_button

    def button_clicked(self, index):
        print("I was clicked from", index.row(), index.column())
