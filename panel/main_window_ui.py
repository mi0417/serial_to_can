# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)
import img_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.serialBox = QComboBox(self.centralwidget)
        self.serialBox.setObjectName(u"serialBox")
        self.serialBox.setGeometry(QRect(20, 30, 80, 23))
        self.connectButton = QPushButton(self.centralwidget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(120, 30, 75, 23))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 80, 581, 341))
        self.resetButton = QPushButton(self.groupBox)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setGeometry(QRect(30, 30, 75, 23))
        self.getConfigButton = QPushButton(self.groupBox)
        self.getConfigButton.setObjectName(u"getConfigButton")
        self.getConfigButton.setGeometry(QRect(120, 30, 75, 23))
        self.setConfigButton = QPushButton(self.groupBox)
        self.setConfigButton.setObjectName(u"setConfigButton")
        self.setConfigButton.setGeometry(QRect(210, 30, 75, 23))
        self.readConfigButton = QPushButton(self.groupBox)
        self.readConfigButton.setObjectName(u"readConfigButton")
        self.readConfigButton.setGeometry(QRect(300, 30, 75, 23))
        self.DIDEdit = QLineEdit(self.groupBox)
        self.DIDEdit.setObjectName(u"DIDEdit")
        self.DIDEdit.setGeometry(QRect(30, 60, 61, 21))
        self.dataEdit = QLineEdit(self.groupBox)
        self.dataEdit.setObjectName(u"dataEdit")
        self.dataEdit.setGeometry(QRect(102, 60, 271, 21))
        self.readDIDButton = QPushButton(self.groupBox)
        self.readDIDButton.setObjectName(u"readDIDButton")
        self.readDIDButton.setGeometry(QRect(390, 60, 75, 23))
        self.writeDIDButton = QPushButton(self.groupBox)
        self.writeDIDButton.setObjectName(u"writeDIDButton")
        self.writeDIDButton.setGeometry(QRect(480, 60, 75, 23))
        self.oneKeyButton = QPushButton(self.groupBox)
        self.oneKeyButton.setObjectName(u"oneKeyButton")
        self.oneKeyButton.setGeometry(QRect(480, 30, 75, 23))
        self.outputWidget = QListWidget(self.groupBox)
        self.outputWidget.setObjectName(u"outputWidget")
        self.outputWidget.setGeometry(QRect(30, 90, 521, 231))
        self.swVerEdit = QLineEdit(self.centralwidget)
        self.swVerEdit.setObjectName(u"swVerEdit")
        self.swVerEdit.setGeometry(QRect(530, 0, 113, 21))
        self.swVerEdit.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Serial2CAN", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"temp", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"reset", None))
        self.getConfigButton.setText(QCoreApplication.translate("MainWindow", u"get config", None))
        self.setConfigButton.setText(QCoreApplication.translate("MainWindow", u"set config", None))
        self.readConfigButton.setText(QCoreApplication.translate("MainWindow", u"read config", None))
        self.DIDEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"DID", None))
        self.dataEdit.setInputMask("")
        self.dataEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"data", None))
        self.readDIDButton.setText(QCoreApplication.translate("MainWindow", u"read", None))
        self.writeDIDButton.setText(QCoreApplication.translate("MainWindow", u"write", None))
        self.oneKeyButton.setText(QCoreApplication.translate("MainWindow", u"one key", None))
    # retranslateUi

