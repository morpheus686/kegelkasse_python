from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow
from ui_maindow import Ui_MainWindow
from controller import MainWindowController, MainWindowModel


class MainWindow(QMainWindow):
    loaded = Signal()
      
    def __init__(self, model: MainWindowModel):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.controller = MainWindowController(model, self)
        
        self._initialized = False

    def showEvent(self, event):   
        super().showEvent(event)   
        
        if not self._initialized: 
            self.loaded.emit()
            self._initialized = True
            print("Main window shown")