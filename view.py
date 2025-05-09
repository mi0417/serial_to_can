'''
view 类
'''
import ctypes
import logging
import os
from PySide6.QtGui import QColor, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QListWidgetItem, QFileDialog, QTextEdit, QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QSize, QMetaObject, Q_ARG, Slot, QTimer


from panel.basic_main_window_ui import Ui_MainWindow

from utils.serial_handle import SerialOperator
from utils.file_utils import exe_absolute_path
from datetime import datetime

logger = logging.getLogger(__name__)
class MyComboBox(QComboBox):

    def __init__(self, parent = None):
        super(MyComboBox,self).__init__(parent) #调用父类初始化方法

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

class MyTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.scrollbar = self.verticalScrollBar()
        self._message_queue = []  # 消息队列
        self._processing = False  # 处理状态标志
        self._lock = False  # 简单锁机制

    def append_text(self, text):
        # 将消息加入队列
        self._message_queue.append(text)
        # 如果不在处理中，触发处理
        if not self._lock:
            self._process_queue()

    @Slot()
    def _process_queue(self):
        if self._message_queue:
            self._lock = True  # 加锁
            text = self._message_queue.pop(0)
             # 添加方法存在性检查
            if hasattr(self, '_safe_append'):
                # 使用AutoConnection自动选择连接方式
                QMetaObject.invokeMethod(self, '_safe_append',
                                       Qt.ConnectionType.AutoConnection,
                                       Q_ARG(str, text))
            else:
                logger.error("_safe_append method not found!")
            self._lock = False  # 解锁
            # 继续处理队列
            QMetaObject.invokeMethod(self, '_process_queue', 
                                   Qt.ConnectionType.QueuedConnection)
            

    @Slot(str)
    def _safe_append(self, text):
        """线程安全的追加文本方法"""
        logger.debug("执行_safe_append方法，文本长度: %d", len(text))
        current_value = self.scrollbar.value()
        max_value = self.scrollbar.maximum()
        is_at_bottom = current_value >= max_value - 4
        
        # 实际插入文本
        super().insertPlainText(f'\n{text}' if not self.document().isEmpty() else text)
        
        # 处理滚动逻辑
        new_max_value = self.scrollbar.maximum()
        if is_at_bottom:
            self.scrollbar.setValue(new_max_value)


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

    LOG_RECEIVE = 'receive'
    LOG_SEND = 'send'

    ASCII = 'ASCII'
    HEX = 'Hex'

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
        self.config_path = None
        self.auto_scroll = True
        self.load_last_config()  # 初始化加载


    def init_UI(self):
        '''
        初始化界面
        '''
        # 设置列表部件允许换行
        self.ui.outputWidget.setWordWrap(True)
        # 添加高度自适应逻辑
        QTimer.singleShot(0, lambda: 
            self.ui.changePageBtn.setMaximumHeight(
                self.ui.changePageBtn.height()
            ))
        
        # 重写QComboBox
        self.ui.serialBox = self.replace_combo_box(self.ui.serialBox, self)
        self.ui.logEdit = self.replace_text_edit(self.ui.logEdit, self)

        # 连接按钮信号
        self.ui.serialBox.currentIndexChanged.connect(lambda: self.show_selected_combobox(self.ui.serialBox))
        self.ui.selectConfigBtn.clicked.connect(self.handle_select_config)
        self.ui.clearLogBtn.clicked.connect(self.clear_log)
        self.ui.saveLogBtn.clicked.connect(self.save_log)
        self.ui.inputConfigBtn.clicked.connect(self.handle_input_config)
        self.ui.scrollBottomBtn.clicked.connect(self.on_scroll_bottom_clicked)
        self.ui.changePageBtn.clicked.connect(self.handle_change_page)
        self.update_change_button_text()  # 初始化按钮文本


    def replace_combo_box(self, original_combo:QComboBox, parent):
        if original_combo:
            logger.debug('替换原有的 QComboBox')
            combo = MyComboBox(parent)
            # combo.setGeometry(original_combo.geometry())
            # combo.addItems([original_combo.itemText(i) for i in range(original_combo.count())])
            # combo.setMinimumSize(original_combo.minimumSize())
            combo.setMaximumSize(original_combo.maximumSize())
            # combo.setFont(original_combo.font())
            # combo.setInputMethodHints(original_combo.inputMethodHints())
            combo.setObjectName(original_combo.objectName())
        else:
            logger.debug('创建新的 QComboBox')
            combo = MyComboBox(parent)
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
    
    def replace_text_edit(self, original_edit:QComboBox, parent):
        if original_edit:
            logger.debug('替换原有的 QTextEdit')
            text_edit = MyTextEdit(parent)
            text_edit.setObjectName(original_edit.objectName())
        else:
            logger.debug('创建新的 QTextEdit')
            text_edit = MyTextEdit(parent)
            text_edit.setObjectName('logEdit')

        # 替换原有的 QTextEdit
        if original_edit.parent().layout():
            index = original_edit.parent().layout().indexOf(original_edit)
            original_edit.parent().layout().removeWidget(original_edit)
            # 释放原有的 QTextEdit 资源
            original_edit.deleteLater()
            original_edit.parent().layout().insertWidget(index, text_edit)
        return text_edit

    def show_selected_combobox(self, combobox:QComboBox):
        '''
        显示选择的combobox的内容
        '''
        selected_index = combobox.currentIndex()
        selected_input = combobox.currentText()
        if selected_input:
            logger.debug('Selected %s: %d - %s', combobox.objectName(), selected_index, selected_input)

    def disable_operation_buttons(self):
        """禁用所有功能操作按钮"""
        self.ui.getSwVerButton.setEnabled(False)
        self.ui.resetButton.setEnabled(False)
        self.ui.setConfigButton.setEnabled(False)
        self.ui.getConfigButton.setEnabled(False)
        self.ui.oneKeyButton.setEnabled(False)
        self.ui.getKeyStatusButton.setEnabled(False)

    def enable_operation_buttons(self):
        """启用所有功能操作按钮""" 
        self.ui.getSwVerButton.setEnabled(True)
        self.ui.resetButton.setEnabled(True)
        self.ui.setConfigButton.setEnabled(True)
        self.ui.getConfigButton.setEnabled(True)
        self.ui.oneKeyButton.setEnabled(True)
        self.ui.getKeyStatusButton.setEnabled(True)

    def handle_change_page(self):
        """处理页面切换按钮点击事件"""
        current_widget = self.ui.stackedWidget.currentWidget()
        
        if current_widget == self.ui.configPage:
            self.ui.stackedWidget.setCurrentWidget(self.ui.logPage)
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.configPage)
        
        self.update_change_button_text()

    def update_change_button_text(self):
        """更新切换按钮文本"""
        current_widget = self.ui.stackedWidget.currentWidget()
        btn_text = "配置" if current_widget == self.ui.logPage else "串口log"
        self.ui.changePageBtn.setText(btn_text)

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

    def handle_input_config(self):
        '''
        处理导入配置文件按钮点击事件
        '''
        # 获取配置文件路径
        config_path = self.ui.configFilePathEdit.text()
        
        if not config_path:
            self.append_to_output_widget('配置文件路径为空', self.LOG_TYPE_ERROR)
            return
            
        # 检查文件是否存在
        if os.path.exists(config_path):
            self.append_to_output_widget(f'导入成功: {config_path}', self.LOG_TYPE_INFO)
            self.config_path = config_path
        else:
            self.append_to_output_widget(f'导入失败，文件不存在: {config_path}', self.LOG_TYPE_ERROR)

    def append_to_output_widget(self, message, log_type=LOG_TYPE_INFO):
        '''
        向界面的 listwidget 末尾添加日志信息，并滚动到最下方。
        当列表项数量超过 MAX_LOG_ITEMS 时，删除最早的项。

        :param message: 要添加的日志信息
        :param log_type: 日志类型，默认为 INFO
        '''
        if not message:
            return
        
        output_widget = self.ui.outputWidget
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
            case self.LOG_TYPE_ERROR:
                item.setForeground(QColor(self.COLOR_RED))

        output_widget.addItem(item)
        output_widget.scrollToBottom()
        logger.debug('log_type:%s, log: %s', log_type, message)

    def on_scroll_bottom_clicked(self):
        """滚动到底部按钮点击事件处理"""
        self.auto_scroll = True
        self.ui.logEdit.verticalScrollBar().setValue(
            self.ui.logEdit.verticalScrollBar().maximum() + 20
        )

    def append_to_log_edit(self, message, log_time=None, type=LOG_RECEIVE, decode=ASCII):
        '''
        向logEdit添加日志信息，并滚动到最下方。

        :param message: 要添加的日志信息
        :param type: 日志类型，默认为receive(LOG_RECEIVE, LOG_SEND)
        :param decode: 解码方式，默认为ASCII(ASCII, HEX)
        '''
        if not message:
            return
            
        if log_time:
            current_time = log_time
        else:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        if type and decode:
            # 添加方向箭头符号  
            direction = ' >>' if type == self.LOG_SEND else ' <<'
            log_message = f'{current_time} - {decode} - {type}{direction}\n{message}'
        else:
            log_message = f'{current_time} - {message}'

        # 使用信号槽机制确保线程安全
        self.ui.logEdit.append_text(f'{log_message}')
        # QMetaObject.invokeMethod(self.ui.logEdit, 'insertPlainText', 
        #                        Qt.ConnectionType.QueuedConnection, 
        #                        Q_ARG(str, f'\n{log_message}'))
        logger.debug('log: %s', message)

    def log(self, message, log_type=LOG_TYPE_INFO, write_to_output=True, write_to_logedit=True):
        '''
        向界面的 listwidget 和/或 textEdit 添加日志信息，并滚动到最下方。
        当列表项数量超过 MAX_LOG_ITEMS 时，删除最早的项。

        :param message: 要添加的日志信息
        :param log_type: 日志类型，默认为 INFO
        :param write_to_output: 是否写入outputWidget，默认为True
        :param write_to_logedit: 是否写入logEdit，默认为True
        '''
        if not message:
            return
            
        if write_to_output:
            self.append_to_output_widget(message, log_type)
        
        if write_to_logedit and self.ui.logEdit:
            self.append_to_log_edit(message)

    def handle_select_config(self):
        '''
        处理选择配置文件按钮点击事件
        '''
        
        # 获取当前路径
        current_path = self.ui.configFilePathEdit.text()
        dir_path = os.path.dirname(current_path) if current_path and os.path.exists(current_path) else ''
        
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择配置文件', dir_path, '配置文件 (*.toml)')
            
        if file_path:
            self.ui.configFilePathEdit.setText(file_path)
            self.handle_input_config()

    
    def clear_log(self):
        '''
        清空日志
        '''
        self.ui.logEdit.clear()
    
    def save_log(self):
        '''
        保存日志到文件
        '''
        
        # 获取日志内容
        log_content = self.ui.logEdit.toPlainText()
        if not log_content:
            self.write_to_statusbar('没有日志内容可保存', True)
            return
            
        # 打开文件保存对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存日志', '', '日志文件 (*.log);;所有文件 (*)')
            
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                self.write_to_statusbar(f'日志已成功保存到 {file_path}')
            except Exception as e:
                self.write_to_statusbar(f'保存日志失败: {str(e)}', True)
    
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

    def load_last_config(self):
        """加载上次保存的配置文件路径"""
        config_file = exe_absolute_path('last_config.ini')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.config_path = f.read().strip()
                    if self.config_path:
                        self.ui.configFilePathEdit.setText(self.config_path)
                        logger.info('加载配置路径: %s', self.config_path)
                        self.handle_input_config()
            except Exception as e:
                logger.error('加载历史配置失败: %s', e)

    def save_last_config(self):
        """保存当前配置文件路径"""
        config_file = exe_absolute_path('last_config.ini')
        try:
            with open(config_file, 'w') as f:
                if self.config_path:
                    f.write(self.config_path)
                    logger.info('保存配置路径: %s', self.config_path)
        except Exception as e:
            logger.error('保存配置路径失败: %s', e)

    def closeEvent(self, event):
        try:
            self.save_last_config()
            self.controller.cleanup()
            logger.debug('Controller ID in SerialView: %s', id(self.controller))
            logger.debug('程序退出')
        except Exception as e:
            logger.error('关闭事件处理时发生错误: %s', e)
        event.accept()