'''
view 类
'''
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QListWidgetItem

from basic_main_window_ui2 import Ui_MainWindow

from logger import logger
from datetime import datetime



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
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        if window_title:
            self.setWindowTitle(window_title)
        self.init_UI()
        self.ui.serialBox.currentIndexChanged.connect(lambda: self.show_selected_combobox(self.ui.serialBox))


    def init_UI(self):
        '''
        初始化界面
        '''
        # 设置列表部件允许换行
        self.ui.outputWidget.setWordWrap(True)


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