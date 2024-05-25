# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditPlayerPenaltyViewYGuJlu.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QSizePolicy, QSpinBox, QTableView, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(467, 186)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.full_spin_box = QSpinBox(Dialog)
        self.full_spin_box.setObjectName(u"full_spin_box")
        self.full_spin_box.setMaximum(800)

        self.gridLayout.addWidget(self.full_spin_box, 0, 1, 1, 1)

        self.clear_spin_box = QSpinBox(Dialog)
        self.clear_spin_box.setObjectName(u"clear_spin_box")
        self.clear_spin_box.setMaximum(300)

        self.gridLayout.addWidget(self.clear_spin_box, 1, 1, 1, 1)

        self.error_spin_box = QSpinBox(Dialog)
        self.error_spin_box.setObjectName(u"error_spin_box")
        self.error_spin_box.setMaximum(120)

        self.gridLayout.addWidget(self.error_spin_box, 3, 1, 1, 1)

        self.total_line_edit = QLineEdit(Dialog)
        self.total_line_edit.setObjectName(u"total_line_edit")
        self.total_line_edit.setReadOnly(True)

        self.gridLayout.addWidget(self.total_line_edit, 2, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.penaltyTable = QTableView(Dialog)
        self.penaltyTable.setObjectName(u"penaltyTable")
        self.penaltyTable.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.penaltyTable, 0, 1, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Spieler bearbeiten", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Abr\u00e4umen", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Gesamt", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Fehler", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Volle", None))
    # retranslateUi

