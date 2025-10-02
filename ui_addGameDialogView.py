# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addGameDialogViewrAdZqS.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateEdit, QDialog,
    QDialogButtonBox, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QSpinBox,
    QTableView, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(470, 260)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.opponentLineEdit = QLineEdit(Dialog)
        self.opponentLineEdit.setObjectName(u"opponentLineEdit")

        self.gridLayout_3.addWidget(self.opponentLineEdit, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)

        self.dateEdit = QDateEdit(Dialog)
        self.dateEdit.setObjectName(u"dateEdit")

        self.gridLayout_3.addWidget(self.dateEdit, 0, 1, 1, 1)

        self.daySpinBox = QSpinBox(Dialog)
        self.daySpinBox.setObjectName(u"daySpinBox")

        self.gridLayout_3.addWidget(self.daySpinBox, 2, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.playerTtableView = QTableView(Dialog)
        self.playerTtableView.setObjectName(u"playerTtableView")

        self.gridLayout.addWidget(self.playerTtableView, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.playerHeader = QLabel(Dialog)
        self.playerHeader.setObjectName(u"playerHeader")

        self.gridLayout.addWidget(self.playerHeader, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        QWidget.setTabOrder(self.dateEdit, self.opponentLineEdit)
        QWidget.setTabOrder(self.opponentLineEdit, self.playerTtableView)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Spieltag anlegen", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Spiel", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Datum", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Gegner", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Spieltag", None))
        self.playerHeader.setText(QCoreApplication.translate("Dialog", u"Spieler f\u00fcr das Spiel", None))
    # retranslateUi

