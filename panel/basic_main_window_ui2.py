# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'basic_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import ctypes

from PySide6.QtCore import (QCoreApplication,
    QMetaObject, QRect,
    QSize, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QAbstractItemView, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QListWidget,
    QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

from panel.my_QWidget import MyComboBoxControl

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("serial2can")
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 600)
        icon = QIcon()
        icon.addFile(u"imgs/icon (2).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 70))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.serialBox = MyComboBoxControl(self.widget)
        self.serialBox.setObjectName(u"serialBox")
        self.serialBox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.serialBox)

        self.connectButton = QPushButton(self.widget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.connectButton)

        self.swVerLabel = QLabel(self.widget)
        self.swVerLabel.setObjectName(u"swVerLabel")
        self.swVerLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.swVerLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.horizontalLayout.addWidget(self.swVerLabel)


        self.verticalLayout.addWidget(self.widget)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.getSwVerButton = QPushButton(self.groupBox)
        self.getSwVerButton.setObjectName(u"getSwVerButton")

        self.horizontalLayout_2.addWidget(self.getSwVerButton)

        self.resetButton = QPushButton(self.groupBox)
        self.resetButton.setObjectName(u"resetButton")

        self.horizontalLayout_2.addWidget(self.resetButton)

        self.setConfigButton = QPushButton(self.groupBox)
        self.setConfigButton.setObjectName(u"setConfigButton")

        self.horizontalLayout_2.addWidget(self.setConfigButton)

        self.getConfigButton = QPushButton(self.groupBox)
        self.getConfigButton.setObjectName(u"getConfigButton")

        self.horizontalLayout_2.addWidget(self.getConfigButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.oneKeyButton = QPushButton(self.groupBox)
        self.oneKeyButton.setObjectName(u"oneKeyButton")

        self.horizontalLayout_2.addWidget(self.oneKeyButton)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.getKeyStatusButton = QPushButton(self.groupBox_2)
        self.getKeyStatusButton.setObjectName(u"getKeyStatusButton")

        self.verticalLayout_2.addWidget(self.getKeyStatusButton)

        self.keyWidget = QWidget(self.groupBox_2)
        self.keyWidget.setObjectName(u"keyWidget")
        self.keyWidget.setMaximumSize(QSize(16777215, 160))
        self.gridLayout = QGridLayout(self.keyWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.honorLabel = QLabel(self.keyWidget)
        self.honorLabel.setObjectName(u"honorLabel")
        self.honorLabel.setMaximumSize(QSize(50, 16777215))
        self.honorLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.honorLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.honorLabel, 5, 0, 1, 1)

        self.xiaomiLabel = QLabel(self.keyWidget)
        self.xiaomiLabel.setObjectName(u"xiaomiLabel")
        self.xiaomiLabel.setMaximumSize(QSize(50, 16777215))
        self.xiaomiLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.xiaomiLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.xiaomiLabel, 1, 0, 1, 1)

        self.keyStatusLabel = QLabel(self.keyWidget)
        self.keyStatusLabel.setObjectName(u"keyStatusLabel")
        self.keyStatusLabel.setMinimumSize(QSize(90, 0))
        self.keyStatusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.keyStatusLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.keyStatusLabel, 0, 1, 1, 1)

        self.huaweiFastChargeStatus = QLabel(self.keyWidget)
        self.huaweiFastChargeStatus.setObjectName(u"huaweiFastChargeStatus")
        self.huaweiFastChargeStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.huaweiFastChargeStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.huaweiFastChargeStatus, 4, 2, 1, 1)

        self.vivoKeyStatus = QLabel(self.keyWidget)
        self.vivoKeyStatus.setObjectName(u"vivoKeyStatus")
        self.vivoKeyStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vivoKeyStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.vivoKeyStatus, 3, 1, 1, 1)

        self.honorKeyStatus = QLabel(self.keyWidget)
        self.honorKeyStatus.setObjectName(u"honorKeyStatus")
        self.honorKeyStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.honorKeyStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.honorKeyStatus, 5, 1, 1, 1)

        self.honorFastChargeStatus = QLabel(self.keyWidget)
        self.honorFastChargeStatus.setObjectName(u"honorFastChargeStatus")
        self.honorFastChargeStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.honorFastChargeStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.honorFastChargeStatus, 5, 2, 1, 1)

        self.vivoFastChargeStatus = QLabel(self.keyWidget)
        self.vivoFastChargeStatus.setObjectName(u"vivoFastChargeStatus")
        self.vivoFastChargeStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vivoFastChargeStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.vivoFastChargeStatus, 3, 2, 1, 1)

        self.huaweiKeyStatus = QLabel(self.keyWidget)
        self.huaweiKeyStatus.setObjectName(u"huaweiKeyStatus")
        self.huaweiKeyStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.huaweiKeyStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.huaweiKeyStatus, 4, 1, 1, 1)

        self.huaweiLabel = QLabel(self.keyWidget)
        self.huaweiLabel.setObjectName(u"huaweiLabel")
        self.huaweiLabel.setMaximumSize(QSize(50, 16777215))
        self.huaweiLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.huaweiLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.huaweiLabel, 4, 0, 1, 1)

        self.oppoKeyStatus = QLabel(self.keyWidget)
        self.oppoKeyStatus.setObjectName(u"oppoKeyStatus")
        self.oppoKeyStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.oppoKeyStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.oppoKeyStatus, 2, 1, 1, 1)

        self.xiaomiKeyStatus = QLabel(self.keyWidget)
        self.xiaomiKeyStatus.setObjectName(u"xiaomiKeyStatus")
        self.xiaomiKeyStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.xiaomiKeyStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.xiaomiKeyStatus, 1, 1, 1, 1)

        self.fastCahrgeStatusLabel = QLabel(self.keyWidget)
        self.fastCahrgeStatusLabel.setObjectName(u"fastCahrgeStatusLabel")
        self.fastCahrgeStatusLabel.setMinimumSize(QSize(100, 0))
        self.fastCahrgeStatusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fastCahrgeStatusLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.fastCahrgeStatusLabel, 0, 2, 1, 1)

        self.spaceLabel = QLabel(self.keyWidget)
        self.spaceLabel.setObjectName(u"spaceLabel")
        self.spaceLabel.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.spaceLabel, 0, 0, 1, 1)

        self.xiaomiFastChargeStatus = QLabel(self.keyWidget)
        self.xiaomiFastChargeStatus.setObjectName(u"xiaomiFastChargeStatus")
        self.xiaomiFastChargeStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.xiaomiFastChargeStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.xiaomiFastChargeStatus, 1, 2, 1, 1)

        self.oppoLabel = QLabel(self.keyWidget)
        self.oppoLabel.setObjectName(u"oppoLabel")
        self.oppoLabel.setMaximumSize(QSize(50, 16777215))
        self.oppoLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.oppoLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.oppoLabel, 2, 0, 1, 1)

        self.vivoLabel = QLabel(self.keyWidget)
        self.vivoLabel.setObjectName(u"vivoLabel")
        self.vivoLabel.setMaximumSize(QSize(50, 16777215))
        self.vivoLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.vivoLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.vivoLabel, 3, 0, 1, 1)

        self.oppoFastChargeStatus = QLabel(self.keyWidget)
        self.oppoFastChargeStatus.setObjectName(u"oppoFastChargeStatus")
        self.oppoFastChargeStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.oppoFastChargeStatus.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.gridLayout.addWidget(self.oppoFastChargeStatus, 2, 2, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)

        self.verticalLayout_2.addWidget(self.keyWidget)

        self.outputWidget = QListWidget(self.groupBox_2)
        self.outputWidget.setObjectName(u"outputWidget")
        self.outputWidget.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)

        self.verticalLayout_2.addWidget(self.outputWidget)


        self.verticalLayout.addWidget(self.groupBox_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 560, 33))
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
        self.swVerLabel.setText(QCoreApplication.translate("MainWindow", u"\u8f6f\u4ef6\u7248\u672c\u53f7\n"
"\u8f6f\u4ef6\u7248\u672c\u53f7", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u914d\u7f6e", None))
        self.getSwVerButton.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u8f6f\u4ef6\u7248\u672c\u53f7", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"\u590d\u4f4d", None))
#if QT_CONFIG(tooltip)
        self.setConfigButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u8fdb\u884c\u590d\u4f4d\uff0c\u914d\u7f6e\u53c2\u6570\u5e76\u786e\u8ba4\u53c2\u6570", None))
#endif // QT_CONFIG(tooltip)
        self.setConfigButton.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u914d\u7f6e", None))
        self.getConfigButton.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u914d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.oneKeyButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u8bfb\u7248\u672c\u53f7\uff0c\u914d\u7f6e\u53c2\u6570\uff0c\u6253\u5370\u8bfb\u53d6\u53c2\u6570", None))
#endif // QT_CONFIG(tooltip)
        self.oneKeyButton.setText(QCoreApplication.translate("MainWindow", u"\u4e00\u952e\u914d\u7f6e", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c", None))
        self.getKeyStatusButton.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u5bc6\u94a5\u72b6\u6001", None))
        self.honorLabel.setText(QCoreApplication.translate("MainWindow", u"\u8363\u8000", None))
        self.xiaomiLabel.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u7c73", None))
        self.keyStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u94a5\u4e0b\u8f7d\u72b6\u6001", None))
        self.huaweiFastChargeStatus.setText("")
        self.vivoKeyStatus.setText("")
        self.honorKeyStatus.setText("")
        self.honorFastChargeStatus.setText("")
        self.vivoFastChargeStatus.setText("")
        self.huaweiKeyStatus.setText("")
        self.huaweiLabel.setText(QCoreApplication.translate("MainWindow", u"\u534e\u4e3a", None))
        self.oppoKeyStatus.setText("")
        self.xiaomiKeyStatus.setText("")
        self.fastCahrgeStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u5145\u529f\u80fd\u5f00\u542f\u72b6\u6001", None))
        self.spaceLabel.setText("")
        self.xiaomiFastChargeStatus.setText("")
        self.oppoLabel.setText(QCoreApplication.translate("MainWindow", u"OPPO", None))
        self.vivoLabel.setText(QCoreApplication.translate("MainWindow", u"vivo", None))
        self.oppoFastChargeStatus.setText("")
    # retranslateUi

