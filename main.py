import sys
from pathlib import Path
from PySide6.QtCore import QFile
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QMainWindow
from qt_material import apply_stylesheet
from controller import MainWindowController
from main_window import Ui_MainWindow
from model import MainWindowModel

start_with_qml = False

if __name__ == '__main__':
    if start_with_qml:
        app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()

        qml_file = Path(__file__).parent / "main.qml"
        absolute = qml_file.resolve().absolute()
        engine.load(absolute)

        app.exec()
    else:
        app = QApplication(sys.argv)

        ui_file = Path(__file__).parent / "main.ui"
        absolute = QFile(ui_file.resolve().absolute())
        window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)

        MainWindowController(MainWindowModel('strafenkatalog.db'), ui)
        window.show()

        apply_stylesheet(app, "light_blue.xml", invert_secondary=True)
        app.exec()
