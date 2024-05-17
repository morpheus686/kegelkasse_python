import sys
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = QQuickView()

    qml_file = Path(__file__).parent / "view.qml"
    absolute =  qml_file.resolve().absolute()
    view.setSource(QUrl.fromLocalFile(absolute))

    errors = view.errors()

    for error in errors:
        print(error)

    view.show()
    app.exec()
