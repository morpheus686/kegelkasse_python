from PySide6.QtGui import Qt
from PySide6.QtWidgets import QStyledItemDelegate, QSpinBox


class SpinBoxDelegate(QStyledItemDelegate):
    """A delegate that allows the user to change integer values from the model
       using a spin box widget. """
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, editor: QSpinBox, index):
        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        editor.setValue(value)

    def setModelData(self, editor: QSpinBox, model, index):
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor: QSpinBox, option, index):
        editor.setGeometry(option.rect)
