from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

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