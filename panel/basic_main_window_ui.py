# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'basic_main_window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QCommandLinkButton,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(625, 800)
        icon = QIcon()
        icon.addFile(u"imgs/icon (2).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 0))
        self.widget.setMaximumSize(QSize(16777215, 90))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 6, 9, 0)
        self.serialBox = QComboBox(self.widget)
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

        self.changePageBtn = QCommandLinkButton(self.widget)
        self.changePageBtn.setObjectName(u"changePageBtn")
        self.changePageBtn.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.changePageBtn)


        self.verticalLayout.addWidget(self.widget)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.configPage = QWidget()
        self.configPage.setObjectName(u"configPage")
        self.verticalLayout_2 = QVBoxLayout(self.configPage)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.groupBox_3 = QGroupBox(self.configPage)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.configFilePathEdit = QLineEdit(self.groupBox_3)
        self.configFilePathEdit.setObjectName(u"configFilePathEdit")

        self.horizontalLayout_3.addWidget(self.configFilePathEdit)

        self.selectConfigBtn = QPushButton(self.groupBox_3)
        self.selectConfigBtn.setObjectName(u"selectConfigBtn")

        self.horizontalLayout_3.addWidget(self.selectConfigBtn)

        self.inputConfigBtn = QPushButton(self.groupBox_3)
        self.inputConfigBtn.setObjectName(u"inputConfigBtn")

        self.horizontalLayout_3.addWidget(self.inputConfigBtn)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.configPage)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_3 = QWidget(self.groupBox)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.getSwVerButton = QPushButton(self.widget_3)
        self.getSwVerButton.setObjectName(u"getSwVerButton")

        self.horizontalLayout_5.addWidget(self.getSwVerButton)

        self.resetButton = QPushButton(self.widget_3)
        self.resetButton.setObjectName(u"resetButton")

        self.horizontalLayout_5.addWidget(self.resetButton)

        self.setConfigButton = QPushButton(self.widget_3)
        self.setConfigButton.setObjectName(u"setConfigButton")
        self.setConfigButton.setMouseTracking(False)

        self.horizontalLayout_5.addWidget(self.setConfigButton)

        self.getConfigButton = QPushButton(self.widget_3)
        self.getConfigButton.setObjectName(u"getConfigButton")

        self.horizontalLayout_5.addWidget(self.getConfigButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.oneKeyButton = QPushButton(self.widget_3)
        self.oneKeyButton.setObjectName(u"oneKeyButton")

        self.horizontalLayout_5.addWidget(self.oneKeyButton)


        self.verticalLayout_5.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.groupBox)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.configTypeLabel = QLabel(self.widget_4)
        self.configTypeLabel.setObjectName(u"configTypeLabel")

        self.horizontalLayout_2.addWidget(self.configTypeLabel)

        self.keyRadioButton = QRadioButton(self.widget_4)
        self.keyRadioButton.setObjectName(u"keyRadioButton")
        self.keyRadioButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.keyRadioButton)

        self.qiRadioButton = QRadioButton(self.widget_4)
        self.qiRadioButton.setObjectName(u"qiRadioButton")

        self.horizontalLayout_2.addWidget(self.qiRadioButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addWidget(self.widget_4)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.configPage)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.getKeyStatusButton = QPushButton(self.groupBox_2)
        self.getKeyStatusButton.setObjectName(u"getKeyStatusButton")

        self.verticalLayout_3.addWidget(self.getKeyStatusButton)

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

        self.verticalLayout_3.addWidget(self.keyWidget)

        self.outputWidget = QListWidget(self.groupBox_2)
        self.outputWidget.setObjectName(u"outputWidget")
        self.outputWidget.setSelectionMode(QAbstractItemView.SelectionMode.ContiguousSelection)

        self.verticalLayout_3.addWidget(self.outputWidget)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.stackedWidget.addWidget(self.configPage)
        self.logPage = QWidget()
        self.logPage.setObjectName(u"logPage")
        self.verticalLayout_4 = QVBoxLayout(self.logPage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_2 = QWidget(self.logPage)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.clearLogBtn = QPushButton(self.widget_2)
        self.clearLogBtn.setObjectName(u"clearLogBtn")

        self.horizontalLayout_4.addWidget(self.clearLogBtn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.scrollBottomBtn = QPushButton(self.widget_2)
        self.scrollBottomBtn.setObjectName(u"scrollBottomBtn")

        self.horizontalLayout_4.addWidget(self.scrollBottomBtn)

        self.saveLogBtn = QPushButton(self.widget_2)
        self.saveLogBtn.setObjectName(u"saveLogBtn")

        self.horizontalLayout_4.addWidget(self.saveLogBtn)


        self.verticalLayout_4.addWidget(self.widget_2)

        self.logEdit = QTextEdit(self.logPage)
        self.logEdit.setObjectName(u"logEdit")
        self.logEdit.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.logEdit)

        self.stackedWidget.addWidget(self.logPage)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 625, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Serial2CAN", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.swVerLabel.setText("")
        self.changePageBtn.setText(QCoreApplication.translate("MainWindow", u"\u4e32\u53e3log", None))
#if QT_CONFIG(tooltip)
        self.stackedWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u8bbe\u7f6e\u6587\u4ef6", None))
        self.selectConfigBtn.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.inputConfigBtn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u8bbe\u7f6e", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u914d\u7f6e", None))
        self.getSwVerButton.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u8f6f\u4ef6\u7248\u672c\u53f7", None))
        self.resetButton.setText(QCoreApplication.translate("MainWindow", u"\u590d\u4f4d", None))
#if QT_CONFIG(tooltip)
        self.setConfigButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u8fdb\u884c\u590d\u4f4d\uff0c\u914d\u7f6e\u53c2\u6570\u5e76\u786e\u8ba4\u53c2\u6570", None))
#endif // QT_CONFIG(tooltip)
        self.setConfigButton.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u914d\u7f6e", None))
        self.getConfigButton.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u914d\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.oneKeyButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e\u53c2\u6570\uff0c\u6253\u5370\u8bfb\u53d6\u53c2\u6570", None))
#endif // QT_CONFIG(tooltip)
        self.oneKeyButton.setText(QCoreApplication.translate("MainWindow", u"\u4e00\u952e\u914d\u7f6e", None))
        self.configTypeLabel.setText(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e\u7c7b\u578b", None))
        self.keyRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u79c1\u6709\u534f\u8bae\u5bc6\u94a5\u4e0b\u8f7d", None))
        self.qiRadioButton.setText(QCoreApplication.translate("MainWindow", u"Qi\u8bc1\u4e66\u4e0b\u8f7d", None))
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
        self.clearLogBtn.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a", None))
        self.scrollBottomBtn.setText(QCoreApplication.translate("MainWindow", u"\u6eda\u52a8\u5230\u7ed3\u5c3e", None))
        self.saveLogBtn.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
    # retranslateUi

