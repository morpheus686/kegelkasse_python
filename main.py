import sys
import main_window
from PySide6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from model import MainWindowModel
from qasync import QEventLoop
import asyncio

if __name__ == '__main__':
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
