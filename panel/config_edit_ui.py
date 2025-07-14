# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_edit.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_configEditWindow(object):
    def setupUi(self, configEditWindow):
        if not configEditWindow.objectName():
            configEditWindow.setObjectName(u"configEditWindow")
        configEditWindow.resize(550, 580)
        self.importAction = QAction(configEditWindow)
        self.importAction.setObjectName(u"importAction")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.importAction.setIcon(icon)
        self.saveAction = QAction(configEditWindow)
        self.saveAction.setObjectName(u"saveAction")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.saveAction.setIcon(icon1)
        self.saveAsAction = QAction(configEditWindow)
        self.saveAsAction.setObjectName(u"saveAsAction")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs))
        self.saveAsAction.setIcon(icon2)
        self.centralwidget = QWidget(configEditWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_4 = QWidget(self.centralwidget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.communicatGroupBox = QGroupBox(self.widget_4)
        self.communicatGroupBox.setObjectName(u"communicatGroupBox")
        self.communicatGroupBox.setMinimumSize(QSize(192, 0))
        self.gridLayout = QGridLayout(self.communicatGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.communicatGroupBox)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.typeComboBox = QComboBox(self.communicatGroupBox)
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.setObjectName(u"typeComboBox")

        self.gridLayout.addWidget(self.typeComboBox, 0, 1, 1, 1)

        self.label_2 = QLabel(self.communicatGroupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.baudrateComboBox = QComboBox(self.communicatGroupBox)
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.setObjectName(u"baudrateComboBox")
        self.baudrateComboBox.setEditable(True)

        self.gridLayout.addWidget(self.baudrateComboBox, 1, 1, 1, 1)

        self.baudrateUnit = QLabel(self.communicatGroupBox)
        self.baudrateUnit.setObjectName(u"baudrateUnit")
        self.baudrateUnit.setMaximumSize(QSize(40, 16777215))

        self.gridLayout.addWidget(self.baudrateUnit, 1, 2, 1, 1)


        self.horizontalLayout_4.addWidget(self.communicatGroupBox)

        self.diagGroupBox = QGroupBox(self.widget_4)
        self.diagGroupBox.setObjectName(u"diagGroupBox")
        self.gridLayout_3 = QGridLayout(self.diagGroupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.requestIDlineEdit = QLineEdit(self.diagGroupBox)
        self.requestIDlineEdit.setObjectName(u"requestIDlineEdit")
        self.requestIDlineEdit.setMaximumSize(QSize(16777215, 16777215))
        self.requestIDlineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.requestIDlineEdit, 0, 1, 1, 1)

        self.label_5 = QLabel(self.diagGroupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)

        self.responseIDlineEdit = QLineEdit(self.diagGroupBox)
        self.responseIDlineEdit.setObjectName(u"responseIDlineEdit")
        self.responseIDlineEdit.setMaximumSize(QSize(16777215, 16777215))
        self.responseIDlineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.responseIDlineEdit, 2, 1, 1, 1)

        self.label_4 = QLabel(self.diagGroupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.diagGroupBox)

        self.qiTransmissionGroupBox = QGroupBox(self.widget_4)
        self.qiTransmissionGroupBox.setObjectName(u"qiTransmissionGroupBox")
        self.gridLayout_2 = QGridLayout(self.qiTransmissionGroupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_6 = QLabel(self.qiTransmissionGroupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 0))
        self.label_6.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.qiTransmitIDlineEdit = QLineEdit(self.qiTransmissionGroupBox)
        self.qiTransmitIDlineEdit.setObjectName(u"qiTransmitIDlineEdit")
        self.qiTransmitIDlineEdit.setMaximumSize(QSize(16777215, 16777215))
        self.qiTransmitIDlineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.qiTransmitIDlineEdit, 0, 1, 1, 1)

        self.label_7 = QLabel(self.qiTransmissionGroupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)

        self.qiReceiveIDlineEdit = QLineEdit(self.qiTransmissionGroupBox)
        self.qiReceiveIDlineEdit.setObjectName(u"qiReceiveIDlineEdit")
        self.qiReceiveIDlineEdit.setMaximumSize(QSize(16777215, 16777215))
        self.qiReceiveIDlineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.qiReceiveIDlineEdit, 1, 1, 1, 1)


        self.horizontalLayout_4.addWidget(self.qiTransmissionGroupBox)


        self.verticalLayout_3.addWidget(self.widget_4)

        self.DIDgroupBox = QGroupBox(self.centralwidget)
        self.DIDgroupBox.setObjectName(u"DIDgroupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.DIDgroupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_13 = QLabel(self.DIDgroupBox)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.getKeyStatusDIDlineEdit = QLineEdit(self.DIDgroupBox)
        self.getKeyStatusDIDlineEdit.setObjectName(u"getKeyStatusDIDlineEdit")

        self.horizontalLayout_3.addWidget(self.getKeyStatusDIDlineEdit)

        self.label_14 = QLabel(self.DIDgroupBox)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_3.addWidget(self.label_14)

        self.readWriteKeyDIDlineEdit = QLineEdit(self.DIDgroupBox)
        self.readWriteKeyDIDlineEdit.setObjectName(u"readWriteKeyDIDlineEdit")

        self.horizontalLayout_3.addWidget(self.readWriteKeyDIDlineEdit)

        self.label_15 = QLabel(self.DIDgroupBox)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_3.addWidget(self.label_15)

        self.getQiStatusDIDlineEdit = QLineEdit(self.DIDgroupBox)
        self.getQiStatusDIDlineEdit.setObjectName(u"getQiStatusDIDlineEdit")

        self.horizontalLayout_3.addWidget(self.getQiStatusDIDlineEdit)


        self.verticalLayout_3.addWidget(self.DIDgroupBox)

        self.NMConfigGroupBox = QGroupBox(self.centralwidget)
        self.NMConfigGroupBox.setObjectName(u"NMConfigGroupBox")
        self.NMConfigGroupBox.setMinimumSize(QSize(420, 350))
        self.verticalLayout = QVBoxLayout(self.NMConfigGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_3 = QWidget(self.NMConfigGroupBox)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.nmEnabledCheckBox = QCheckBox(self.widget_3)
        self.nmEnabledCheckBox.setObjectName(u"nmEnabledCheckBox")
        self.nmEnabledCheckBox.setMaximumSize(QSize(50, 16777215))
        self.nmEnabledCheckBox.setChecked(True)

        self.horizontalLayout_2.addWidget(self.nmEnabledCheckBox)

        self.label_12 = QLabel(self.widget_3)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_2.addWidget(self.label_12)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget = QWidget(self.NMConfigGroupBox)
        self.widget.setObjectName(u"widget")
        self.gridLayout_4 = QGridLayout(self.widget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 0, 7, 1, 1)

        self.NMDLCcomboBox = QComboBox(self.widget)
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.addItem("")
        self.NMDLCcomboBox.setObjectName(u"NMDLCcomboBox")

        self.gridLayout_4.addWidget(self.NMDLCcomboBox, 0, 8, 1, 1)

        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.NMIDlineEdit = QLineEdit(self.widget)
        self.NMIDlineEdit.setObjectName(u"NMIDlineEdit")
        self.NMIDlineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_4.addWidget(self.NMIDlineEdit, 0, 1, 1, 1)

        self.NMPeriodLineEdit = QLineEdit(self.widget)
        self.NMPeriodLineEdit.setObjectName(u"NMPeriodLineEdit")
        self.NMPeriodLineEdit.setMinimumSize(QSize(0, 0))
        self.NMPeriodLineEdit.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_4.addWidget(self.NMPeriodLineEdit, 0, 4, 1, 1)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 0, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 9, 1, 1)


        self.verticalLayout.addWidget(self.widget)

        self.groupBox_5 = QGroupBox(self.NMConfigGroupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_2 = QWidget(self.groupBox_5)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.readNMDataLineEdit = QLineEdit(self.widget_2)
        self.readNMDataLineEdit.setObjectName(u"readNMDataLineEdit")

        self.horizontalLayout.addWidget(self.readNMDataLineEdit)

        self.recognizeNMDataButton = QPushButton(self.widget_2)
        self.recognizeNMDataButton.setObjectName(u"recognizeNMDataButton")

        self.horizontalLayout.addWidget(self.recognizeNMDataButton)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.NMDataTableWidget = QTableWidget(self.groupBox_5)
        if (self.NMDataTableWidget.columnCount() < 8):
            self.NMDataTableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.NMDataTableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.NMDataTableWidget.rowCount() < 8):
            self.NMDataTableWidget.setRowCount(8)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(4, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(5, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(6, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.NMDataTableWidget.setVerticalHeaderItem(7, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 4, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 5, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 6, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(0, 7, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 2, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 3, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 4, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 5, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 6, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(1, 7, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 0, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 1, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 2, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 3, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 4, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 5, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 6, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(2, 7, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 0, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 1, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 2, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 3, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 4, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 5, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 6, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(3, 7, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 0, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 1, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 2, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 3, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 4, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 5, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 6, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(4, 7, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 0, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 1, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 2, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 3, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 4, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 5, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 6, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(5, 7, __qtablewidgetitem63)
        __qtablewidgetitem64 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 0, __qtablewidgetitem64)
        __qtablewidgetitem65 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 1, __qtablewidgetitem65)
        __qtablewidgetitem66 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 2, __qtablewidgetitem66)
        __qtablewidgetitem67 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 3, __qtablewidgetitem67)
        __qtablewidgetitem68 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 4, __qtablewidgetitem68)
        __qtablewidgetitem69 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 5, __qtablewidgetitem69)
        __qtablewidgetitem70 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 6, __qtablewidgetitem70)
        __qtablewidgetitem71 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(6, 7, __qtablewidgetitem71)
        __qtablewidgetitem72 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 0, __qtablewidgetitem72)
        __qtablewidgetitem73 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 1, __qtablewidgetitem73)
        __qtablewidgetitem74 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 2, __qtablewidgetitem74)
        __qtablewidgetitem75 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 3, __qtablewidgetitem75)
        __qtablewidgetitem76 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 4, __qtablewidgetitem76)
        __qtablewidgetitem77 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 5, __qtablewidgetitem77)
        __qtablewidgetitem78 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 6, __qtablewidgetitem78)
        __qtablewidgetitem79 = QTableWidgetItem()
        self.NMDataTableWidget.setItem(7, 7, __qtablewidgetitem79)
        self.NMDataTableWidget.setObjectName(u"NMDataTableWidget")
        self.NMDataTableWidget.setAutoScrollMargin(16)
        self.NMDataTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.NMDataTableWidget.horizontalHeader().setDefaultSectionSize(55)
        self.NMDataTableWidget.verticalHeader().setDefaultSectionSize(23)

        self.verticalLayout_2.addWidget(self.NMDataTableWidget)


        self.verticalLayout.addWidget(self.groupBox_5)


        self.verticalLayout_3.addWidget(self.NMConfigGroupBox)

        configEditWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(configEditWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 550, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        configEditWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(configEditWindow)
        self.statusbar.setObjectName(u"statusbar")
        configEditWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.importAction)
        self.menu.addSeparator()
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.saveAsAction)

        self.retranslateUi(configEditWindow)

        self.NMDLCcomboBox.setCurrentIndex(15)


        QMetaObject.connectSlotsByName(configEditWindow)
    # setupUi

    def retranslateUi(self, configEditWindow):
        configEditWindow.setWindowTitle(QCoreApplication.translate("configEditWindow", u"\u914d\u7f6e\u6587\u4ef6\u7f16\u8f91", None))
        self.importAction.setText(QCoreApplication.translate("configEditWindow", u"\u5bfc\u5165...", None))
        self.saveAction.setText(QCoreApplication.translate("configEditWindow", u"\u4fdd\u5b58", None))
        self.saveAsAction.setText(QCoreApplication.translate("configEditWindow", u"\u53e6\u5b58\u4e3a", None))
        self.communicatGroupBox.setTitle(QCoreApplication.translate("configEditWindow", u"\u901a\u4fe1\u914d\u7f6e", None))
        self.label.setText(QCoreApplication.translate("configEditWindow", u"\u901a\u4fe1\u7c7b\u578b", None))
        self.typeComboBox.setItemText(0, QCoreApplication.translate("configEditWindow", u"CAN", None))
        self.typeComboBox.setItemText(1, QCoreApplication.translate("configEditWindow", u"CANFD", None))
        self.typeComboBox.setItemText(2, QCoreApplication.translate("configEditWindow", u"LIN", None))
        self.typeComboBox.setItemText(3, QCoreApplication.translate("configEditWindow", u"Uart", None))

        self.label_2.setText(QCoreApplication.translate("configEditWindow", u"\u6ce2\u7279\u7387", None))
        self.baudrateComboBox.setItemText(0, QCoreApplication.translate("configEditWindow", u"125", None))
        self.baudrateComboBox.setItemText(1, QCoreApplication.translate("configEditWindow", u"250", None))
        self.baudrateComboBox.setItemText(2, QCoreApplication.translate("configEditWindow", u"500", None))
        self.baudrateComboBox.setItemText(3, QCoreApplication.translate("configEditWindow", u"1000", None))
        self.baudrateComboBox.setItemText(4, QCoreApplication.translate("configEditWindow", u"2000", None))
        self.baudrateComboBox.setItemText(5, QCoreApplication.translate("configEditWindow", u"4000", None))
        self.baudrateComboBox.setItemText(6, QCoreApplication.translate("configEditWindow", u"5000", None))
        self.baudrateComboBox.setItemText(7, QCoreApplication.translate("configEditWindow", u"8000", None))

        self.baudrateUnit.setText(QCoreApplication.translate("configEditWindow", u"K bps", None))
        self.diagGroupBox.setTitle(QCoreApplication.translate("configEditWindow", u"\u8bca\u65ad\u914d\u7f6e\uff0811-Bit ID\uff09", None))
        self.requestIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x", None))
        self.label_5.setText(QCoreApplication.translate("configEditWindow", u"\u5e94\u7b54ID", None))
        self.responseIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x", None))
        self.label_4.setText(QCoreApplication.translate("configEditWindow", u"\u8bf7\u6c42ID", None))
        self.qiTransmissionGroupBox.setTitle(QCoreApplication.translate("configEditWindow", u"Qi\u8bc1\u4e66\u900f\u4f20", None))
        self.label_6.setText(QCoreApplication.translate("configEditWindow", u"\u53d1\u9001ID", None))
        self.qiTransmitIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x7F0", None))
        self.label_7.setText(QCoreApplication.translate("configEditWindow", u"\u63a5\u6536ID", None))
        self.qiReceiveIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x7F1", None))
        self.DIDgroupBox.setTitle(QCoreApplication.translate("configEditWindow", u"\u5bc6\u94a5\u8bfb\u5199DID", None))
        self.label_13.setText(QCoreApplication.translate("configEditWindow", u"\u83b7\u53d6\u5bc6\u94a5\u72b6\u6001", None))
        self.getKeyStatusDIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x4209", None))
        self.label_14.setText(QCoreApplication.translate("configEditWindow", u"\u8bfb\u5199\u534e\u4e3a\u8363\u8000", None))
        self.readWriteKeyDIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x420A", None))
        self.label_15.setText(QCoreApplication.translate("configEditWindow", u"\u83b7\u53d6Qi\u5bc6\u94a5\u72b6\u6001", None))
        self.getQiStatusDIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x420D", None))
        self.NMConfigGroupBox.setTitle(QCoreApplication.translate("configEditWindow", u"\u7f51\u7edc\u7ba1\u7406\u62a5\u6587", None))
        self.nmEnabledCheckBox.setText(QCoreApplication.translate("configEditWindow", u"\u4f7f\u80fd", None))
        self.label_12.setText(QCoreApplication.translate("configEditWindow", u"\uff08\u76ee\u524d\u53ea\u652f\u63018\u548c64\u5b57\u8282\uff09", None))
        self.label_11.setText(QCoreApplication.translate("configEditWindow", u"DLC", None))
        self.NMDLCcomboBox.setItemText(0, QCoreApplication.translate("configEditWindow", u"0", None))
        self.NMDLCcomboBox.setItemText(1, QCoreApplication.translate("configEditWindow", u"1", None))
        self.NMDLCcomboBox.setItemText(2, QCoreApplication.translate("configEditWindow", u"2", None))
        self.NMDLCcomboBox.setItemText(3, QCoreApplication.translate("configEditWindow", u"3", None))
        self.NMDLCcomboBox.setItemText(4, QCoreApplication.translate("configEditWindow", u"4", None))
        self.NMDLCcomboBox.setItemText(5, QCoreApplication.translate("configEditWindow", u"5", None))
        self.NMDLCcomboBox.setItemText(6, QCoreApplication.translate("configEditWindow", u"6", None))
        self.NMDLCcomboBox.setItemText(7, QCoreApplication.translate("configEditWindow", u"7", None))
        self.NMDLCcomboBox.setItemText(8, QCoreApplication.translate("configEditWindow", u"8", None))
        self.NMDLCcomboBox.setItemText(9, QCoreApplication.translate("configEditWindow", u"9", None))
        self.NMDLCcomboBox.setItemText(10, QCoreApplication.translate("configEditWindow", u"10", None))
        self.NMDLCcomboBox.setItemText(11, QCoreApplication.translate("configEditWindow", u"11", None))
        self.NMDLCcomboBox.setItemText(12, QCoreApplication.translate("configEditWindow", u"12", None))
        self.NMDLCcomboBox.setItemText(13, QCoreApplication.translate("configEditWindow", u"13", None))
        self.NMDLCcomboBox.setItemText(14, QCoreApplication.translate("configEditWindow", u"14", None))
        self.NMDLCcomboBox.setItemText(15, QCoreApplication.translate("configEditWindow", u"15", None))

        self.label_8.setText(QCoreApplication.translate("configEditWindow", u"\u62a5\u6587ID", None))
        self.NMIDlineEdit.setText(QCoreApplication.translate("configEditWindow", u"0x", None))
        self.label_10.setText(QCoreApplication.translate("configEditWindow", u"ms", None))
        self.label_9.setText(QCoreApplication.translate("configEditWindow", u"\u5468\u671f", None))
        self.groupBox_5.setTitle("")
        self.readNMDataLineEdit.setInputMask("")
        self.readNMDataLineEdit.setText("")
        self.readNMDataLineEdit.setPlaceholderText(QCoreApplication.translate("configEditWindow", u"\u7c98\u8d34\u62a5\u6587\u5230\u8fd9\u91cc\u8fdb\u884c\u8bc6\u522b", None))
        self.recognizeNMDataButton.setText(QCoreApplication.translate("configEditWindow", u"\u8bc6\u522b\u62a5\u6587", None))
        ___qtablewidgetitem = self.NMDataTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("configEditWindow", u"0", None));
        ___qtablewidgetitem1 = self.NMDataTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("configEditWindow", u"1", None));
        ___qtablewidgetitem2 = self.NMDataTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("configEditWindow", u"2", None));
        ___qtablewidgetitem3 = self.NMDataTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("configEditWindow", u"3", None));
        ___qtablewidgetitem4 = self.NMDataTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("configEditWindow", u"4", None));
        ___qtablewidgetitem5 = self.NMDataTableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("configEditWindow", u"5", None));
        ___qtablewidgetitem6 = self.NMDataTableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("configEditWindow", u"6", None));
        ___qtablewidgetitem7 = self.NMDataTableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("configEditWindow", u"7", None));
        ___qtablewidgetitem8 = self.NMDataTableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("configEditWindow", u"0", None));
        ___qtablewidgetitem9 = self.NMDataTableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("configEditWindow", u"8", None));
        ___qtablewidgetitem10 = self.NMDataTableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("configEditWindow", u"16", None));
        ___qtablewidgetitem11 = self.NMDataTableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("configEditWindow", u"24", None));
        ___qtablewidgetitem12 = self.NMDataTableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("configEditWindow", u"32", None));
        ___qtablewidgetitem13 = self.NMDataTableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("configEditWindow", u"40", None));
        ___qtablewidgetitem14 = self.NMDataTableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("configEditWindow", u"48", None));
        ___qtablewidgetitem15 = self.NMDataTableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("configEditWindow", u"56", None));

        __sortingEnabled = self.NMDataTableWidget.isSortingEnabled()
        self.NMDataTableWidget.setSortingEnabled(False)
        ___qtablewidgetitem16 = self.NMDataTableWidget.item(0, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem17 = self.NMDataTableWidget.item(0, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem18 = self.NMDataTableWidget.item(0, 2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem19 = self.NMDataTableWidget.item(0, 3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem20 = self.NMDataTableWidget.item(0, 4)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem21 = self.NMDataTableWidget.item(0, 5)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem22 = self.NMDataTableWidget.item(0, 6)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem23 = self.NMDataTableWidget.item(0, 7)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem24 = self.NMDataTableWidget.item(1, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem25 = self.NMDataTableWidget.item(1, 1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem26 = self.NMDataTableWidget.item(1, 2)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem27 = self.NMDataTableWidget.item(1, 3)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem28 = self.NMDataTableWidget.item(1, 4)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem29 = self.NMDataTableWidget.item(1, 5)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem30 = self.NMDataTableWidget.item(1, 6)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem31 = self.NMDataTableWidget.item(1, 7)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem32 = self.NMDataTableWidget.item(2, 0)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem33 = self.NMDataTableWidget.item(2, 1)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem34 = self.NMDataTableWidget.item(2, 2)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem35 = self.NMDataTableWidget.item(2, 3)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem36 = self.NMDataTableWidget.item(2, 4)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem37 = self.NMDataTableWidget.item(2, 5)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem38 = self.NMDataTableWidget.item(2, 6)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem39 = self.NMDataTableWidget.item(2, 7)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem40 = self.NMDataTableWidget.item(3, 0)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem41 = self.NMDataTableWidget.item(3, 1)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem42 = self.NMDataTableWidget.item(3, 2)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem43 = self.NMDataTableWidget.item(3, 3)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem44 = self.NMDataTableWidget.item(3, 4)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem45 = self.NMDataTableWidget.item(3, 5)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem46 = self.NMDataTableWidget.item(3, 6)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem47 = self.NMDataTableWidget.item(3, 7)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem48 = self.NMDataTableWidget.item(4, 0)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem49 = self.NMDataTableWidget.item(4, 1)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem50 = self.NMDataTableWidget.item(4, 2)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem51 = self.NMDataTableWidget.item(4, 3)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem52 = self.NMDataTableWidget.item(4, 4)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem53 = self.NMDataTableWidget.item(4, 5)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem54 = self.NMDataTableWidget.item(4, 6)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem55 = self.NMDataTableWidget.item(4, 7)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem56 = self.NMDataTableWidget.item(5, 0)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem57 = self.NMDataTableWidget.item(5, 1)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem58 = self.NMDataTableWidget.item(5, 2)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem59 = self.NMDataTableWidget.item(5, 3)
        ___qtablewidgetitem59.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem60 = self.NMDataTableWidget.item(5, 4)
        ___qtablewidgetitem60.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem61 = self.NMDataTableWidget.item(5, 5)
        ___qtablewidgetitem61.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem62 = self.NMDataTableWidget.item(5, 6)
        ___qtablewidgetitem62.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem63 = self.NMDataTableWidget.item(5, 7)
        ___qtablewidgetitem63.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem64 = self.NMDataTableWidget.item(6, 0)
        ___qtablewidgetitem64.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem65 = self.NMDataTableWidget.item(6, 1)
        ___qtablewidgetitem65.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem66 = self.NMDataTableWidget.item(6, 2)
        ___qtablewidgetitem66.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem67 = self.NMDataTableWidget.item(6, 3)
        ___qtablewidgetitem67.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem68 = self.NMDataTableWidget.item(6, 4)
        ___qtablewidgetitem68.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem69 = self.NMDataTableWidget.item(6, 5)
        ___qtablewidgetitem69.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem70 = self.NMDataTableWidget.item(6, 6)
        ___qtablewidgetitem70.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem71 = self.NMDataTableWidget.item(6, 7)
        ___qtablewidgetitem71.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem72 = self.NMDataTableWidget.item(7, 0)
        ___qtablewidgetitem72.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem73 = self.NMDataTableWidget.item(7, 1)
        ___qtablewidgetitem73.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem74 = self.NMDataTableWidget.item(7, 2)
        ___qtablewidgetitem74.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem75 = self.NMDataTableWidget.item(7, 3)
        ___qtablewidgetitem75.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem76 = self.NMDataTableWidget.item(7, 4)
        ___qtablewidgetitem76.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem77 = self.NMDataTableWidget.item(7, 5)
        ___qtablewidgetitem77.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem78 = self.NMDataTableWidget.item(7, 6)
        ___qtablewidgetitem78.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        ___qtablewidgetitem79 = self.NMDataTableWidget.item(7, 7)
        ___qtablewidgetitem79.setText(QCoreApplication.translate("configEditWindow", u"00", None));
        self.NMDataTableWidget.setSortingEnabled(__sortingEnabled)

        self.menu.setTitle(QCoreApplication.translate("configEditWindow", u"\u9009\u9879", None))
    # retranslateUi

