import sys
import main_window
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from model import MainWindowModel
from qasync import QEventLoop

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)   
    model = MainWindowModel('Kegelkasse.db')
    window = main_window.MainWindow(model)
    window.show()
    apply_stylesheet(app, "light_blue.xml", invert_secondary=False)
    app.exec()
