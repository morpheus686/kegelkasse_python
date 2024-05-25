# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainKypWbc.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1109, 603)
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

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setFont(font)

        self.verticalLayout.addWidget(self.tableView)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1109, 22))
        self.menuEinstellungen = QMenu(self.menuBar)
        self.menuEinstellungen.setObjectName(u"menuEinstellungen")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuEinstellungen.menuAction())
        self.menuEinstellungen.addAction(self.actionMannschaften_verwalten)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Kegel-Strafenkatalog", None))
        self.actionMannschaften_verwalten.setText(QCoreApplication.translate("MainWindow", u"Mannschaften verwalten", None))
        self.previous_push_button.setText("")
        self.game_day_label.setText(QCoreApplication.translate("MainWindow", u"Spieltag vom xx.xx.xxxx", None))
        self.next_push_button.setText("")
        self.menuEinstellungen.setTitle(QCoreApplication.translate("MainWindow", u"Einstellungen", None))
    # retranslateUi

