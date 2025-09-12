import sys
import main_window
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from model import MainWindowModel
from qasync import QEventLoop
import asyncio

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
        loop = QEventLoop(app)    
        asyncio.set_event_loop(loop)
        model = MainWindowModel('Kegelkasse.db')
        window = main_window.MainWindow(model)
        window.show()
        apply_stylesheet(app, "light_blue.xml", invert_secondary=True)
        app.exec()
        
        with loop:
            loop.run_forever()
