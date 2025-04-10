'''
view 类
'''
import ctypes
import logging
from PySide6.QtGui import QColor, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QListWidgetItem
from PySide6.QtCore import Qt, QSize

from panel.basic_main_window_ui import Ui_MainWindow

from utils.serial_handle import SerialOperator
from datetime import datetime

logger = logging.getLogger(__name__)
class MyComboBoxControl(QComboBox):

    def __init__(self, parent = None):
        super(MyComboBoxControl,self).__init__(parent) #调用父类初始化方法

    # 重写showPopup函数
    def showPopup(self):  
        # 获取原选项
        index = self.currentIndex()
        logger.debug('当前索引:%d', index)
        font_metrics = QFontMetrics(self.font())
        # 先清空原有的选项
        self.clear()
        # 初始化串口列表
        available_ports = SerialOperator().list_available_ports(True)
        logger.info('可用串口:%s', available_ports)
        # 计算滚动条宽度
        scrollbar_width = self.view().verticalScrollBar().sizeHint().width()
        # 计算视图的内边距
        view_margins = self.view().contentsMargins()
        total_margin_width = view_margins.left() + view_margins.right()
        max_width = 0
        for port in available_ports:
            self.addItem(port)

            # width = font_metrics.horizontalAdvance (port) + 30
            # 计算文本的宽度
            text_width = font_metrics.horizontalAdvance(port)
            # 计算包含滚动条和内边距的总宽度
            width = text_width + scrollbar_width + total_margin_width + 10
            if width > max_width:
                max_width = width

        if max_width > self.maximumWidth():
            self.view().setFixedWidth(max_width)

        if self.count() >= index:
            self.setCurrentIndex(index)
            logger.debug('重置串口数据，设置索引:%d', index)
        QComboBox.showPopup(self)   # 弹出选项框  

class View(QMainWindow):
    # view 颜色
    COLOR_GREEN = '#00FF00'
    COLOR_RED = '#FF0000'
    COLOR_BLUE = '#0000FF'
    COLOR_YELLOW = '#FFFF00'
    COLOR_ORANGE = '#FFA500'
    COLOR_PURPLE = '#800080'
    COLOR_CYAN = '#00FFFF'
    COLOR_MAGENTA = '#FF00FF'
    COLOR_BROWN = '#A52A2A'
    COLOR_GRAY = '#808080'
    COLOR_LIGHT_GRAY = '#D3D3D3'

    BTN_CONNECT = '连接'
    BTN_DISCONNECT = '断开连接'

    LOG_TYPE_INFO = 0
    LOG_TYPE_DATA = 1
    LOG_TYPE_ERROR = 2

    MAX_LOG_ITEMS = 500  # 设定最大日志项数
    def __init__(self, icon_path = None, window_title = None):
        super().__init__()
        self.controller = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("serial2can")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        if window_title:
            self.setWindowTitle(window_title)
            
        self.init_UI()


    def init_UI(self):
        '''
        初始化界面
        '''
        # 设置列表部件允许换行
        self.ui.outputWidget.setWordWrap(True)
        
        # 重写QComboBox
        self.ui.serialBox = self.replace_combo_box(self.ui.serialBox, self)


        self.ui.serialBox.currentIndexChanged.connect(lambda: self.show_selected_combobox(self.ui.serialBox))


    def replace_combo_box(self, original_combo:QComboBox, parent):
        if original_combo:
            logger.debug('替换原有的 QComboBox')
            combo = MyComboBoxControl(parent)
            # combo.setGeometry(original_combo.geometry())
            # combo.addItems([original_combo.itemText(i) for i in range(original_combo.count())])
            # combo.setMinimumSize(original_combo.minimumSize())
            combo.setMaximumSize(original_combo.maximumSize())
            # combo.setFont(original_combo.font())
            # combo.setInputMethodHints(original_combo.inputMethodHints())
            combo.setObjectName(original_combo.objectName())
        else:
            logger.debug('创建新的 QComboBox')
            combo = MyComboBoxControl(parent)
            # combo.setMinimumSize(QSize(180, 25))
            combo.setMaximumSize(QSize(100, 16777215))
            # font = QFont()
            # font.setFamily('微软雅黑')
            # font.setPointSize(20)
            # combo.setFont(font)
            # combo.setInputMethodHints(Qt.ImhEmailCharactersOnly | Qt.ImhNoAutoUppercase)
            combo.setObjectName('serialBox')

        # 替换原有的 QComboBox
        if original_combo.parent().layout():
            index = original_combo.parent().layout().indexOf(original_combo)
            original_combo.parent().layout().removeWidget(original_combo)
            # 释放原有的 QComboBox 资源
            original_combo.deleteLater()
            original_combo.parent().layout().insertWidget(index, combo)
        return combo

    def show_selected_combobox(self, combobox:QComboBox):
        '''
        显示选择的combobox的内容
        '''
        selected_index = combobox.currentIndex()
        selected_input = combobox.currentText()
        if selected_input:
            logger.debug('Selected %s: %d - %s', combobox.objectName(), selected_index, selected_input)

    def change_button_text(self, button:QPushButton, text):
        '''
        改变按钮的文本
        '''
        button.setText(text)

    def change_label_text(self, label:QLabel, text, color=None):
        '''
        改变标签的文本
        '''
        label.setText(text)
        if color:
            label.setStyleSheet(f'color: {color};')
        else:
            label.setStyleSheet('')

    def log_message(self, message, log_type=LOG_TYPE_INFO):
        '''
        向界面的 listwidget 末尾添加日志信息，并滚动到最下方。
        当列表项数量超过 MAX_LOG_ITEMS 时，删除最早的项。

        :param message: 要添加的日志信息
        :param is_error: 是否为错误消息，默认为 False
        '''
        # 假设 listwidget 的对象名为 logListWidget，根据实际情况修改
        output_widget = self.ui.outputWidget
        if message:
            if output_widget.count() >= self.MAX_LOG_ITEMS:
                # 删除最早的项
                item = output_widget.takeItem(0)
                del item
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_message = f'{current_time} - {message}'
            item = QListWidgetItem(str(log_message))
            match log_type:
                case self.LOG_TYPE_INFO:
                    item.setForeground(QColor(self.COLOR_GRAY))
                # case self.LOG_TYPE_DATA:
                #     item.setForeground(QColor(QBrush()))
                case self.LOG_TYPE_ERROR:
                    item.setForeground(QColor(self.COLOR_RED))

            output_widget.addItem(item)
            output_widget.scrollToBottom()
            logger.debug('log_list: %s', message)

    def write_to_statusbar(self, message, is_error=False):
        '''
        向 statusbar 写入带时间的数据。

        :param message: 要显示的消息
        :param is_error: 是否为错误消息，默认为 False
        '''
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_message = f'{current_time} - {message}'
        status_bar = self.statusBar()
        
        status_bar.showMessage(status_message)

        if is_error:
            # 设置红色前景色
            status_bar.setStyleSheet('background-color: red;')
        else:
            # 恢复系统默认颜色
            status_bar.setStyleSheet('')

    def closeEvent(self, event):
        try:
            self.controller.cleanup()
            logger.debug('Controller ID in SerialView: %s', id(self.controller))
            logger.debug('程序退出')
        except Exception as e:
            logger.error('关闭事件处理时发生错误: %s', e)
        event.accept()