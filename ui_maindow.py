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

class Ui_MainWindow(object):     
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(850, 550)
        self.actionMannschaften_verwalten = QAction(MainWindow)
        self.actionMannschaften_verwalten.setObjectName(u"actionMannschaften_verwalten")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.previous_push_button = QPushButton(self.centralwidget)
        self.previous_push_button.setObjectName(u"previous_push_button")
        icon = QIcon(QIcon.fromTheme(u"go-previous"))
        self.previous_push_button.setIcon(icon)

        self.horizontalLayout.addWidget(self.previous_push_button)

        self.game_day_label = QLabel(self.centralwidget)
        self.game_day_label.setObjectName(u"game_day_label")
        font = QFont()
        font.setPointSize(20)
        self.game_day_label.setFont(font)

        self.horizontalLayout.addWidget(self.game_day_label)

        self.next_push_button = QPushButton(self.centralwidget)
        self.next_push_button.setObjectName(u"next_push_button")
        icon1 = QIcon(QIcon.fromTheme(u"go-next"))
        self.next_push_button.setIcon(icon1)

        self.horizontalLayout.addWidget(self.next_push_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 1, 9, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 3, 1, 1)

        self.full_lineEdit = QLineEdit(self.groupBox)
        self.full_lineEdit.setObjectName(u"full_lineEdit")
        self.full_lineEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.full_lineEdit, 0, 4, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)

        self.paysum_lineedit = QLineEdit(self.groupBox)
        self.paysum_lineedit.setObjectName(u"paysum_lineedit")
        self.paysum_lineedit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.paysum_lineedit, 0, 7, 1, 1)

        self.teamerrors_lineEdit = QLineEdit(self.groupBox)
        self.teamerrors_lineEdit.setObjectName(u"teamerrors_lineEdit")
        self.teamerrors_lineEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.teamerrors_lineEdit, 1, 1, 1, 1)

        self.payed_lineedit = QLineEdit(self.groupBox)
        self.payed_lineedit.setObjectName(u"payed_lineedit")
        self.payed_lineedit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.payed_lineedit, 1, 7, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 6, 1, 1)

        self.teamresult_lineedit = QLineEdit(self.groupBox)
        self.teamresult_lineedit.setObjectName(u"teamresult_lineedit")
        self.teamresult_lineedit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.teamresult_lineedit, 0, 1, 1, 1)

        self.clear_lineEdit = QLineEdit(self.groupBox)
        self.clear_lineEdit.setObjectName(u"clear_lineEdit")
        self.clear_lineEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.clear_lineEdit, 1, 4, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 6, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 8, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setFont(font)

        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 950, 22))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RT 2 gem Kegelkasse", None))
        self.actionMannschaften_verwalten.setText(QCoreApplication.translate("MainWindow", u"Mannschaften verwalten", None))
        self.previous_push_button.setText("")
        self.game_day_label.setText(QCoreApplication.translate("MainWindow", u"Spieltag vom xx.xx.xxxx", None))
        self.next_push_button.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Spieldaten", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Abr\u00e4umen", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Volle", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fehler", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Zu zahlen", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Mannschaftsergebnis", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Gezahlt", None))
    # retranslateUi

