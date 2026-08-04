
"""
"""
import os
import logging
from io import StringIO
from datetime import datetime
import toml

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QStyledItemDelegate, QLineEdit, QHeaderView, QFileDialog, QMessageBox, QStyle
from PySide6.QtGui import QIcon, QRegularExpressionValidator, QShortcut, QKeySequence
from PySide6.QtCore import Signal, Qt, QRegularExpression
from PySide6.QtWidgets import QApplication

from panel.config_edit_ui import Ui_configEditWindow
from utils.file_utils import resource_path, read_toml_file, get_exe_dir
from utils.common_data_utils import split_hex_string, int_to_hex_string
from utils.data_processor import ValidValues

logger = logging.getLogger(__name__)

class HexDelegate(QStyledItemDelegate):
    """
    自定义委托类，用于处理表格中十六进制数据的输入和显示。
    该类确保输入为两位十六进制数字，并在黑色主题下优化选中单元格的显示效果。
    """
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        # 设置输入验证规则为两位十六进制数字
        validator = QRegularExpressionValidator(QRegularExpression(r'^[0-9A-Fa-f]{0,2}$'), editor)
        editor.setValidator(validator)
        editor.setAlignment(Qt.AlignCenter)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.EditRole)
        editor.setText(text)

    def setModelData(self, editor, model, index):
        # 获取编辑器中的文本
        text = editor.text()
        # 去除 0x 或 0X 前缀
        if text.startswith(("0x", "0X")):
            text = text[2:]
        # 确保文本为两位大写十六进制
        text = text.upper().zfill(2)
        model.setData(index, text, Qt.EditRole)

    def paint(self, painter, option, index):
        # 检查单元格是否被选中
        # logger.debug(f"Painting cell at {index.row()}, {index.column()} with state {option.state}")
        '''if option.state & QStyle.State_Selected:
            # logger.debug("Cell is selected")
            # 打印选中单元格的样式相关信息
            row = index.row()
            col = index.column()
            print(f"选中的单元格位于第 {row} 行，第 {col} 列")'''
        # 调用父类的 paint 方法进行绘制
        super().paint(painter, option, index)

class ConfigEditWindow(QMainWindow):


    closed = Signal()  # 自定义关闭信号
    EDITDISABLE_TEXT="--"

    DEFAULT_CAN_TYPE = ValidValues.CAN_TYPES[1] #默认CANFD

    def __init__(self, config_file_path=None):

        super().__init__()
        self.ui = Ui_configEditWindow()
        self.ui.setupUi(self)
        self.config_file_path = config_file_path
        # 初始化内部数组，64 个 00
        self.internal_array = ["00"] * 64
        self.is_import_button_clicked = False  # 新增标志位

        # 设置窗口最小高度，允许窗口缩小
        self.setMinimumHeight(650)
        
        self._setup_logo()
        self._connect_signals()
        self._init_table_and_delegate()
        self._setup_input_validators()
        self._setup_default_settings()
        self._setup_hex_input_handlers()
        self._connect_nm_data_button()
        self._connect_file_actions()  # 连接文件操作信号

        # 设置 Ctrl+S 快捷键
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_config)

        if self.config_file_path:
            # 初始化时加载配置
            self.load_config_file(self.config_file_path)

    def _setup_logo(self):
        """加载并设置 logo"""
        logo_path = resource_path('panel/imgs/config_icon.png')
        self.setWindowIcon(QIcon(logo_path))

    def _connect_signals(self):
        """连接信号和槽"""
        self.ui.typeComboBox.currentIndexChanged.connect(self.update_baudrate_settings)
        self.ui.NMDLCcomboBox.currentIndexChanged.connect(self.update_table_editable)
        self.ui.cusdomKeyDIDcheckBox.stateChanged.connect(self._on_cusdom_key_did_checkbox_changed)
        # 设置初始状态：默认不勾选，并应用初始界面逻辑
        self.ui.cusdomKeyDIDcheckBox.setChecked(False)
        self._on_cusdom_key_did_checkbox_changed(False)

    def _setup_default_settings(self):
        """设置默认选项"""
        # 设置 typeComboBox 默认选中 CANFD
        canfd_index = self.ui.typeComboBox.findText(ConfigEditWindow.DEFAULT_CAN_TYPE)
        if canfd_index != -1:
            self.ui.typeComboBox.setCurrentIndex(canfd_index)
            # 调用更新波特率设置的方法
            self.update_baudrate_settings(canfd_index)

        # 根据 NMDLCcomboBox 的初始值初始化表格样式
        initial_dlc = self.ui.NMDLCcomboBox.currentIndex()
        self.update_table_editable(initial_dlc)

    def _init_table_and_delegate(self):
        """初始化表格和设置自定义委托"""
        self.init_table()
        self.delegate = HexDelegate()
        self.ui.NMDataTableWidget.setItemDelegate(self.delegate)

    def _setup_input_validators(self):
        """设置输入验证器"""
        # 设置 baudrateComboBox 只能输入数字
        self.ui.baudrateComboBox.setEditable(True)
        validator_digit = QRegularExpressionValidator(QRegularExpression(r'^\d+$'))
        self.ui.baudrateComboBox.lineEdit().setValidator(validator_digit)

        # 设置 NMPeriodLineEdit 只能输入数字
        validator_digit = QRegularExpressionValidator(QRegularExpression(r'^\d+$'))
        self.ui.NMPeriodLineEdit.setValidator(validator_digit)

    def _setup_hex_input_handlers(self):
        """设置十六进制输入框的验证规则和编辑结束处理"""
        # 定义输入框和对应允许长度的映射
        line_edit_length_mapping = {
            self.ui.requestIDlineEdit: [3, 4],      # [3,4,7]
            self.ui.responseIDlineEdit: [3, 4],     # [3,4,7]
            self.ui.qiTransmitIDlineEdit: [3, 4],
            self.ui.qiReceiveIDlineEdit: [3, 4],
            self.ui.getKeyStatusDIDlineEdit: [4],
            self.ui.readWriteKeyDIDlineEdit: [4],
            self.ui.getQiStatusDIDlineEdit: [4],
            self.ui.NMIDlineEdit: [3, 4],           # [3,4,7]
            # keyDIDWidget 里的 lineEdit
            self.ui.getUIDDIDlineEdit: [4],
            self.ui.readHuaweiDIDlineEdit: [4],
            self.ui.writeHuaweiDIDlineEdit: [4],
            self.ui.readXiaomiKeyDIDlineEdit: [4],
            self.ui.writeXiaomiKeyDIDlineEdit: [4],
            self.ui.readHonorKeyDIDlineEdit: [4],
            self.ui.writeHonorKeyDIDlineEdit: [4],
            self.ui.readQiDIDlineEdit: [4],
            self.ui.writeQiDIDlineEdit: [4],
            self.ui.readOppoKeyDIDlineEdit: [4],
            self.ui.writeOppoKeyDIDlineEdit: [4],
            self.ui.readLuxQiDIDlineEdit: [4],
            self.ui.writeLuxQiDIDlineEdit: [4],
            self.ui.readVivoKeyDIDlineEdit: [4],
            self.ui.writeVivoKeyDIDlineEdit: [4],
        }

        # 设置 requestIDlineEdit，responseIDlineEdit，qiTransmitIDlineEdit 的验证规则和编辑结束处理
        hex_validator = QRegularExpressionValidator(QRegularExpression(r'^(0x)?[0-9A-Fa-f]{3,4}$'))

        # 使用 items() 方法同时获取键和值
        for line_edit, hex_lengths in line_edit_length_mapping.items():
            line_edit.setValidator(hex_validator)
            line_edit.editingFinished.connect(lambda le=line_edit, hl=hex_lengths: self.handle_hex_input(le, hl))
            # line_edit.textChanged.connect(lambda le=line_edit, hl=hex_lengths: self.handle_hex_input(le, hl))

    def _connect_nm_data_button(self):
        """连接 recognizeNMDataButton 的点击信号"""
        self.ui.recognizeNMDataButton.clicked.connect(self.fill_table_from_line)

    def init_table(self):
        """初始化表格，设置 8x8 表格"""
        self.ui.NMDataTableWidget.setRowCount(8)
        self.ui.NMDataTableWidget.setColumnCount(8)
        self.ui.NMDataTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格宽度占满窗口
        header = self.ui.NMDataTableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # 为每个单元格设置居中对齐
        for row in range(8):
            for col in range(8):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)  # 设置单元格内容居中对齐
                self.ui.NMDataTableWidget.setItem(row, col, item)

    def update_table_editable(self, value):
        """根据 NMDLCcomboBox 的值更新表格的可编辑状态"""
        edit_trigger = QAbstractItemView.AllEditTriggers
        self.ui.NMDataTableWidget.setEditTriggers(edit_trigger)

        # 获取可编辑的字节数
        if 0 <= value < len(ValidValues.CAN_DLC_LENGTH):
            editable_bytes = ValidValues.CAN_DLC_LENGTH[value]
        else:
            logger.error("Invalid DLC value: %d", value)
            return

        for row in range(8):
            for col in range(8):
                cell_index = row * 8 + col
                editable = cell_index < editable_bytes
                self._set_cell_editable(row, col, editable=editable)

    def _set_rows_editable(self, start_row, end_row, editable=True):
        """设置指定行范围可编辑"""
        for row in range(start_row, end_row):
            for col in range(self.ui.NMDataTableWidget.columnCount()):
                self._set_cell_editable(row, col, editable=editable)

    def _set_cell_editable(self, row, col, editable=True):
        """设置指定单元格可编辑，文字居中"""
        item = self.ui.NMDataTableWidget.item(row, col)
        if not item:
            item = QTableWidgetItem()
            self.ui.NMDataTableWidget.setItem(row, col, item)

        index = row * 8 + col
        if editable:
            if item.text() == ConfigEditWindow.EDITDISABLE_TEXT:
                item.setText(self.internal_array[index])
            # 可编辑时启用单元格，允许编辑和选择
            item.setFlags(item.flags() | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
            item.setToolTip("此单元格可编辑")
            item.setStatusTip("此单元格可编辑")
        else:
            # 禁用时将可编辑部分的数字放入数组对应位置
            if item.text() != ConfigEditWindow.EDITDISABLE_TEXT:
                self.internal_array[index] = item.text()
            item.setText(ConfigEditWindow.EDITDISABLE_TEXT)
            # 不可编辑时禁用单元格，禁止编辑和选择
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable)
            item.setToolTip("此单元格不可编辑")
            item.setStatusTip("此单元格不可编辑")
        
        # logger.debug(f"设置单元格 ({row}, {col}) 可编辑状态为 {editable}")
        self.ui.NMDataTableWidget.viewport().update()
        # 强制更新表格样式
        self.ui.NMDataTableWidget.style().unpolish(self.ui.NMDataTableWidget.viewport())
        self.ui.NMDataTableWidget.style().polish(self.ui.NMDataTableWidget.viewport())

    def update_baudrate_settings(self, index):
        """
        根据通信类型更新波特率设置
        """
        type_choice = self.ui.typeComboBox.itemText(index)
        baudrate_unit = self.ui.baudrateUnit
        baudrate_combo = self.ui.baudrateComboBox

        if type_choice == ValidValues.CAN_TYPES[0]:
            baudrate_unit.setText("K bps")
            baudrate_combo.clear()
            baudrate_combo.addItems(["125", "250", "500", "1000"])
            baudrate_combo.setCurrentText("500")
        elif type_choice == ValidValues.CAN_TYPES[1]:
            baudrate_unit.setText("K bps")
            baudrate_combo.clear()
            baudrate_combo.addItems(["125", "250", "500", "1000", "2000", "4000", "5000", "8000"])
            baudrate_combo.setCurrentText("2000")
        elif type_choice == ValidValues.CAN_TYPES[2]:
            baudrate_unit.setText("bps")
            baudrate_combo.clear()
            baudrate_combo.addItems(["2400", "4800", "9600", "10417", "19200", "20000"])
            baudrate_combo.setCurrentText("19200")
        elif type_choice == ValidValues.CAN_TYPES[3]:
            baudrate_unit.setText("bps")
            baudrate_combo.clear()
            baudrate_combo.addItems([
                "110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200",
                "38400", "56000", "57600", "115200", "128000", "230400", "256000",
                "460800", "921600", "1000000", "2000000"
            ])
            baudrate_combo.setCurrentText("115200")

    def handle_hex_input(self, line_edit, hex_lengths):
        """
        处理输入的十六进制字符串，确保格式正确
        """
        text = line_edit.text()
        # 处理 0X 前缀，转换为 0x
        if text.startswith("0X"):
            text = "0x" + text[2:]
        if text and not text.startswith("0x"):
            if len(text) in hex_lengths and all(c in "0123456789ABCDEFabcdef" for c in text):
                text = f"0x{text}"
        # 将十六进制部分转换为大写
        if text.startswith("0x"):
            text = "0x" + text[2:].upper()
        line_edit.setText(text)

    def fill_table_from_line(self):
        """
        点击 recognizeNMDataButton 时，将 readNMDataLineEdit 中的十六进制数据填入表格
        """
        input_text = self.ui.readNMDataLineEdit.text()
        self.fill_table_with_hex_data(input_text)
        
    def fill_table_with_hex_data(self, input_text):
        """
        从十六进制字符串中填充表格数据
        """
        if not input_text:
            return
        
        hex_array = split_hex_string(input_text)

        row_count = self.ui.NMDataTableWidget.rowCount()
        col_count = self.ui.NMDataTableWidget.columnCount()
        index = 0

        for row in range(row_count):
            for col in range(col_count):
                if index < len(hex_array):
                    hex_value = hex_array[index].upper()
                    item = self.ui.NMDataTableWidget.item(row, col)
                    if item is None:
                        item = QTableWidgetItem()
                        self.ui.NMDataTableWidget.setItem(row, col, item)
                    # 检查 item 是否可编辑
                    if item.flags() & Qt.ItemIsEditable:
                        item.setText(hex_value)
                        index += 1
                    else:
                        break
                else:
                    break

            if index >= len(hex_array):
                break

    def _clear_qi_login(self):
        """清除Qi账号信息，通过主窗口调用"""
        from view.view import View
        from PySide6.QtWidgets import QApplication

        # 方案1：尝试从父窗口链查找（如果 ConfigEditWindow 曾设置过父窗口）
        parent = self.parent()
        while parent:
            if isinstance(parent, View):
                parent.clear_qi_login()
                return
            parent = parent.parent()

        # 方案2：从应用顶级窗口查找
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, View):
                widget.clear_qi_login()
                return

        # 方案3：通过 objectName 查找（更可靠的方式）
        for widget in QApplication.topLevelWidgets():
            if widget.objectName() == "View":
                widget.clear_qi_login()
                return

        # 方案4：通过窗口标题查找（备选方案）
        for widget in QApplication.topLevelWidgets():
            window_title = widget.windowTitle()
            if window_title and "SerialToCAN" in window_title:
                if isinstance(widget, View):
                    widget.clear_qi_login()
                    return

        logger.warning('未找到主窗口View，无法清除Qi账号')

    def _clear_ui(self):
        """清空界面所有控件，恢复到初始状态"""
        # 清空内部数组
        self.internal_array = ["00"] * 64
        
        # 清空 CAN 配置区域
        self.ui.requestIDlineEdit.setText('')
        self.ui.responseIDlineEdit.setText('')
        
        # 重置 CAN 类型到默认（CANFD），这会自动重置波特率
        canfd_index = self.ui.typeComboBox.findText(ConfigEditWindow.DEFAULT_CAN_TYPE)
        if canfd_index != -1:
            self.ui.typeComboBox.setCurrentIndex(canfd_index)
            self.update_baudrate_settings(canfd_index)
        
        # 清空诊断 DID 配置
        self.ui.getKeyStatusDIDlineEdit.setText('')
        self.ui.readWriteKeyDIDlineEdit.setText('')
        
        # 清空 Qi 证书配置
        self.ui.qiTransmitIDlineEdit.setText('')
        self.ui.qiReceiveIDlineEdit.setText('')
        self.ui.getQiStatusDIDlineEdit.setText('')
        
        # 重置网络管理配置
        self.ui.nmEnabledCheckBox.setChecked(False)
        self.ui.NMDLCcomboBox.setCurrentIndex(0)
        self.update_table_editable(0)  # 重置表格编辑状态
        self.ui.NMIDlineEdit.setText('')
        self.ui.NMPeriodLineEdit.setText('')
        self.ui.NMPeriodLineEdit.setText('100')  # 恢复默认值
        self.ui.readNMDataLineEdit.setText('')
        
        # 清空表格所有数据
        for row in range(8):
            for col in range(8):
                item = self.ui.NMDataTableWidget.item(row, col)
                if item and (item.flags() & Qt.ItemIsEditable):
                    item.setText('')
        
        # 清空 FlashDriver 配置
        self.ui.FlashDriverNameLineEdit.setText('')
        
        # 重置 cusdomKeyDIDcheckBox 为不勾选状态
        if self.ui.cusdomKeyDIDcheckBox.isChecked():
            self.ui.cusdomKeyDIDcheckBox.setChecked(False)
            self._on_cusdom_key_did_checkbox_changed(False)
        
        # 清空 keyDIDWidget 的所有 lineEdit
        self.ui.getUIDDIDlineEdit.setText('0x')
        self.ui.readHuaweiDIDlineEdit.setText('0x')
        self.ui.writeHuaweiDIDlineEdit.setText('0x')
        self.ui.readXiaomiKeyDIDlineEdit.setText('0x')
        self.ui.writeXiaomiKeyDIDlineEdit.setText('0x')
        self.ui.readHonorKeyDIDlineEdit.setText('0x')
        self.ui.writeHonorKeyDIDlineEdit.setText('0x')
        self.ui.readQiDIDlineEdit.setText('0x')
        self.ui.writeQiDIDlineEdit.setText('0x')
        self.ui.readOppoKeyDIDlineEdit.setText('0x')
        self.ui.writeOppoKeyDIDlineEdit.setText('0x')
        self.ui.readLuxQiDIDlineEdit.setText('0x')
        self.ui.writeLuxQiDIDlineEdit.setText('0x')
        self.ui.readVivoKeyDIDlineEdit.setText('0x')
        self.ui.writeVivoKeyDIDlineEdit.setText('0x')
        
        logger.debug("界面已清空")
    
    def _connect_file_actions(self):
        """连接文件操作信号"""
        self.ui.importAction.triggered.connect(self.import_config)
        self.ui.saveAction.triggered.connect(self.save_config)
        self.ui.saveAsAction.triggered.connect(self.save_as_config)
        self.ui.OpenFlashDriverPathButton.clicked.connect(self.open_flash_driver_path)
        
        # 添加清除Qi账号菜单项
        self.clearQiLoginAction = self.ui.menu.addAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton),
            "清除Qi账号"
        )
        self.clearQiLoginAction.triggered.connect(self._clear_qi_login)

    def open_flash_driver_path(self):
        """打开 FlashDriver 目录"""
        flash_driver_dir = os.path.join(get_exe_dir(), ValidValues.FLASH_DRIVER_SECTION)
        if not os.path.exists(flash_driver_dir):
            os.makedirs(flash_driver_dir)
        # 使用系统文件管理器打开目录
        os.startfile(flash_driver_dir)

    def import_config(self):
        """点击导入键导入配置文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "导入配置文件", "", "TOML 文件 (*.toml)")
        if file_path:
            self.is_import_button_clicked = True  # 设置标志位
            self.load_config_file(file_path)
            self.is_import_button_clicked = False  # 重置标志位

    def load_config_file(self, file_path):
        """加载配置文件内容并填充 UI"""
        # 检查路径是否为空
        if not file_path:
            error_msg = "配置文件路径为空"
            logger.error(error_msg)
            self._clear_ui()
            self.fill_ui_and_show_result(None, error_msg)
            return
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            error_msg = f"配置文件 {file_path} 不存在"
            logger.error(error_msg)
            self._clear_ui()
            self.fill_ui_and_show_result(None, error_msg)
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                logger.info("开始导入配置文件: %s", file_path)
                config = read_toml_file(file_path)
                logger.debug("读取到配置：\n%s", config)
            error_msg = None
        except Exception as e:
            config = None
            error_msg = f"导入配置文件 {file_path} 失败: {str(e)}"
            logger.error(error_msg)

        self.config_file_path = file_path
        # 加载配置文件前先清空界面，确保旧配置的数据被清除
        self._clear_ui()
        self.fill_ui_and_show_result(config, error_msg)

    def fill_ui_and_show_result(self, config, error_msg=None):
        """填充 UI 并显示操作结果"""
        import_log = ""
        success = False
        if config:
            fill_log = self._fill_ui_with_config(config)
            success = True
            import_log = f"成功导入配置文件: {self.config_file_path}"
            if fill_log:
                import_log += f"\n\n{fill_log}"
        else:
            if not error_msg:
                error_msg = "导入配置文件失败"
            import_log = error_msg
            self.write_to_statusbar(error_msg, True)

        # 只有在点击导入键或 fill_log 不为空时才弹出消息框
        if self.is_import_button_clicked or (success and fill_log) or not success:
            # 弹出消息框显示导入结果
            msg_box = QMessageBox(self)
            if success:
                msg_box.setIcon(QMessageBox.Information)
                msg_box.setWindowTitle("导入成功")
            else:
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("导入失败")
            msg_box.setText(import_log)
            msg_box.exec()
        self.write_to_statusbar(f'{self.config_file_path}加载完成', not success)


    def _fill_ui_with_config(self, config):
        """根据配置填充 UI"""
        fill_log = ""
        
        # 填充 CAN 配置
        can_config = config.get(ValidValues.CAN_CONFIG_SECTION, {})
        if can_config != {}:
            # 查找 type 值对应的索引
            type_value = can_config.get(ValidValues.CAN_TYPE_KEY, ValidValues.CAN_TYPES[0])
            if type_value:
                type_value = type_value.strip().upper()
                # 查找匹配的索引
                type_index = -1
                for i in range(self.ui.typeComboBox.count()):
                    item_text = self.ui.typeComboBox.itemText(i).strip().upper()
                    if item_text == type_value:
                        type_index = i
                        break
                    
                if type_index != -1:    
                    # 设置对应的选项
                    self.ui.typeComboBox.setCurrentIndex(type_index)
                else:
                    fill_log += f"未找到匹配的 CAN 类型: {can_config.get(ValidValues.CAN_TYPE_KEY, ValidValues.CAN_TYPES[0])}\n"

            baudrate = can_config.get(ValidValues.BAUDRATE_KEY, 0)
            if baudrate != 0:
                baudrate_index = self.ui.typeComboBox.findText(str(baudrate))
                if baudrate_index != -1:
                    # 设置对应的选项
                    self.ui.baudrateComboBox.setCurrentIndex(baudrate_index)
                else:
                    self.ui.baudrateComboBox.setCurrentText(str(baudrate))
            else:
                fill_log += "未找到波特率"

            
            # 检查 request_id 是否存在，存在则更新界面
            request_id = can_config.get(ValidValues.REQUEST_ID_KEY, 0)
            if request_id != 0:
                self.ui.requestIDlineEdit.setText(int_to_hex_string(request_id))
            else:
                fill_log += "未找到请求ID\n"
            
            # 检查 response_id 是否存在，存在则更新界面
            response_id = can_config.get(ValidValues.RESPONSE_ID_KEY, 0)
            if response_id != 0:
                self.ui.responseIDlineEdit.setText(int_to_hex_string(response_id))
            else:
                fill_log += "未找到应答ID\n"
        else:
            fill_log += "未找到CAN配置\n"

        # 填充诊断 DID 配置
        diag_did = config.get(ValidValues.DIAG_DID_SECTION, {})
        if diag_did != {}:
            # 检查 get_key_status 是否存在，存在则更新界面
            get_key_status = diag_did.get(ValidValues.GET_KEY_STATUS_KEY, 0)
            if get_key_status != 0:
                self.ui.getKeyStatusDIDlineEdit.setText(int_to_hex_string(get_key_status))
            else:
                fill_log += "未找到获取密钥状态DID\n"

            # 检查 read_write_key 是否存在，存在则更新界面
            read_write_key = diag_did.get(ValidValues.READ_WRITE_KEY_KEY, 0)
            if read_write_key != 0:
                self.ui.readWriteKeyDIDlineEdit.setText(int_to_hex_string(read_write_key))
            else:
                fill_log += "未找到读写华为荣耀DID\n"
        else:
            fill_log += "未找到诊断DID配置\n"

        # 填充 Qi 证书配置
        qi_config = config.get(ValidValues.QI_CERTIFICATE_SECTION, {})
        if qi_config != {}:
            # 检查 get_qi_status 是否存在，存在则更新界面
            get_qi_status = qi_config.get(ValidValues.GET_QI_STATUS_KEY, 0)
            if get_qi_status != 0:
                self.ui.getQiStatusDIDlineEdit.setText(int_to_hex_string(get_qi_status))
            else:
                fill_log += "未找到获取Qi证书状态DID\n"

            # 检查 qi_transmit_id 是否存在，存在则更新界面
            qi_transmit_id = qi_config.get(ValidValues.QI_TRANSMIT_ID_KEY, 0)
            if qi_transmit_id != 0:
                self.ui.qiTransmitIDlineEdit.setText(int_to_hex_string(qi_transmit_id))
            else:
                fill_log += "未找到Qi证书透传发送ID\n"

            # 检查 qi_receive_id 是否存在，存在则更新界面
            qi_receive_id = qi_config.get(ValidValues.QI_RECEIVE_ID_KEY, 0)
            if qi_receive_id != 0:
                self.ui.qiReceiveIDlineEdit.setText(int_to_hex_string(qi_receive_id))
            else:
                fill_log += "未找到Qi证书透传接收ID\n"
        else:
            fill_log += "未找到Qi证书配置\n"

        # 填充网络管理配置
        nm_config = config.get(ValidValues.NM_CONFIG_SECTION, {})
        if nm_config != {}:
            # 检查 nm_enabled 是否存在，存在则更新界面
            nm_enabled = nm_config.get(ValidValues.NM_ENABLED_KEY, None)
            logger.debug("nm_enabled: %s", nm_enabled)
            if nm_enabled is not None:
                self.ui.nmEnabledCheckBox.setChecked(nm_enabled)
            else:
                fill_log += "未找到网络管理使能状态\n"
            # 检查 nm_DLC 是否存在，存在则更新界面
            nm_DLC = nm_config.get(ValidValues.NM_DLC_KEY, 16)
            if nm_DLC != 16:
                self.ui.NMDLCcomboBox.setCurrentIndex(nm_DLC)
            else:
                fill_log += "未找到网络管理DLC\n"
            # 检查 nm_id 是否存在，存在则更新界面
            nm_id = nm_config.get(ValidValues.NM_ID_KEY, 0)
            if nm_id != 0:
                self.ui.NMIDlineEdit.setText(int_to_hex_string(nm_id))
            else:
                fill_log += "未找到网络管理ID\n"
            # 检查 nm_period 是否存在，存在则更新界面
            nm_period = nm_config.get(ValidValues.NM_PERIOD_KEY, -1)
            if nm_period != -1:
                self.ui.NMPeriodLineEdit.setText(str(nm_period))
            else:
                fill_log += "未找到网络管理周期\n"
            
            # 检查 nm_message 是否存在，存在则更新界面
            nm_message = nm_config.get(ValidValues.NM_MESSAGE_KEY, '')
            if nm_message:
                self.fill_table_with_hex_data(nm_message)
            else:
                fill_log += "未找到网络管理报文信息\n"
        else:
            fill_log += "未找到网络管理配置\n"

        # 填充 FlashDriver 配置（如果存在）
        flash_driver_config = config.get(ValidValues.FLASH_DRIVER_SECTION, {})
        if flash_driver_config:
            flash_driver_name = flash_driver_config.get(ValidValues.FLASH_DRIVER_NAME_KEY, '')
            self.ui.FlashDriverNameLineEdit.setText(flash_driver_name)
        # 如果不存在 FlashDriver 配置，也不报错，保持界面原样
        
        # ============================================
        # CUSTOM_DID_SECTION 处理部分（keyDIDWidget 配置）
        # ============================================
        def fill_custom_did_line_edit(line_edit, value):
            """填充 custom_did 的 lineEdit，0x0、0x0000、0 留空"""
            if value in [0, '0x0', '0x0000']:
                line_edit.setText('')
            elif isinstance(value, int):
                line_edit.setText(f'0x{value:04X}')
            else:
                line_edit.setText(value)
        
        custom_did = config.get(ValidValues.CUSTOM_DID_SECTION, {})
        if custom_did:
            # 先填充 custom_did 配置到 keyDIDWidget 的 lineEdit
            fill_custom_did_line_edit(self.ui.getUIDDIDlineEdit, custom_did.get(ValidValues.GET_UID_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readHuaweiDIDlineEdit, custom_did.get(ValidValues.HUAWEI_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeHuaweiDIDlineEdit, custom_did.get(ValidValues.HUAWEI_WRITE_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readXiaomiKeyDIDlineEdit, custom_did.get(ValidValues.XIAOMI_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeXiaomiKeyDIDlineEdit, custom_did.get(ValidValues.XIAOMI_WRITE_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readHonorKeyDIDlineEdit, custom_did.get(ValidValues.HONOR_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeHonorKeyDIDlineEdit, custom_did.get(ValidValues.HONOR_WRITE_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readQiDIDlineEdit, custom_did.get(ValidValues.QI_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeQiDIDlineEdit, custom_did.get(ValidValues.QI_WRITE_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readOppoKeyDIDlineEdit, custom_did.get(ValidValues.OPPO_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeOppoKeyDIDlineEdit, custom_did.get(ValidValues.OPPO_WRITE_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readLuxQiDIDlineEdit, custom_did.get(ValidValues.LUXQI_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeLuxQiDIDlineEdit, custom_did.get(ValidValues.LUXQI_WRITE_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.readVivoKeyDIDlineEdit, custom_did.get(ValidValues.VIVO_READ_DID_KEY, 0))
            fill_custom_did_line_edit(self.ui.writeVivoKeyDIDlineEdit, custom_did.get(ValidValues.VIVO_WRITE_DID_KEY, 0))
            
            # 最后勾选 cusdomKeyDIDcheckBox，触发 _on_cusdom_key_did_checkbox_changed 执行高度调整和界面更新
            if not self.ui.cusdomKeyDIDcheckBox.isChecked():
                self.ui.cusdomKeyDIDcheckBox.setChecked(True)
        # 如果不存在 custom_did 配置，也不报错，保持界面原样
        
        # ============================================
        # 自动填充逻辑：当 write 行未填写时，自动从 read 行填充值
        # ============================================
        self._auto_fill_write_from_read()
        
        logger.debug("填充配置到界面完成，日志信息: %s", fill_log)
        return fill_log

    def _auto_fill_write_from_read(self):
        """
        自动填充逻辑：当 write 行的 lineEdit 为空时，自动从对应的 read 行填充值
        配对关系：
        1. readHuaweiDIDlineEdit → writeHuaweiDIDlineEdit
        2. readHonorKeyDIDlineEdit → writeHonorKeyDIDlineEdit
        3. readOppoKeyDIDlineEdit → writeOppoKeyDIDlineEdit
        4. readVivoKeyDIDlineEdit → writeVivoKeyDIDlineEdit
        5. readXiaomiKeyDIDlineEdit → writeXiaomiKeyDIDlineEdit
        """
        # 定义 read → write 的配对关系
        read_write_pairs = [
            # (self.ui.readHuaweiDIDlineEdit, self.ui.writeHuaweiDIDlineEdit),
            # (self.ui.readHonorKeyDIDlineEdit, self.ui.writeHonorKeyDIDlineEdit),
            (self.ui.readOppoKeyDIDlineEdit, self.ui.writeOppoKeyDIDlineEdit),
            # (self.ui.readVivoKeyDIDlineEdit, self.ui.writeVivoKeyDIDlineEdit),
            (self.ui.readXiaomiKeyDIDlineEdit, self.ui.writeXiaomiKeyDIDlineEdit),
        ]
        
        # 遍历配对关系，如果 write 为空则从 read 填充
        for read_edit, write_edit in read_write_pairs:
            write_text = write_edit.text().strip()
            if not write_text:
                read_text = read_edit.text().strip()
                if read_text:
                    write_edit.setText(read_text)
                    logger.debug(f"自动填充 write from read: {read_edit.objectName()} -> {write_edit.objectName()}, 值: {read_text}")
            
    def save_config(self):
        """保存配置到原文件"""
        if self.config_file_path:
            try:
                self._save_config_to_file(self.config_file_path)
                self.write_to_statusbar(f"配置已保存到 {self.config_file_path}", False)
                logger.info("配置已保存到 %s", self.config_file_path)
            except Exception as e:
                self.write_to_statusbar(f"保存配置文件失败: {e}", True)
                logger.error("保存配置文件失败: %s", e)
        else:
            self.save_as_config()

    def save_as_config(self):
        """另存为配置文件"""
        file_path, _ = QFileDialog.getSaveFileName(self, "另存为配置文件", "", "TOML 文件 (*.toml)")
        if file_path:
            try:
                self._save_config_to_file(file_path)
                self.config_file_path = file_path
                self.write_to_statusbar(f"配置已保存到 {self.config_file_path}", False)
            except Exception as e:
                self.write_to_statusbar(f"另存为配置文件失败: {e}", True)
                logger.error("另存为配置文件失败: %s", e)

    def _save_config_to_file(self, file_path):
        """将配置保存到指定文件"""
        config = self._get_config_from_ui()
        # 先将配置数据转换为 TOML 格式的字符串
        toml_string = StringIO()
        toml.dump(config, toml_string)
        toml_lines = toml_string.getvalue().splitlines()

        # 定义各配置项对应的注释
        section_comments = {
            ValidValues.CAN_CONFIG_SECTION: "# 配置 CAN 通信相关参数",
            ValidValues.DIAG_DID_SECTION: "# 配置诊断 DID 相关参数",
            ValidValues.QI_CERTIFICATE_SECTION: "# 配置 Qi 证书相关参数",
            ValidValues.NM_CONFIG_SECTION: "# 配置网络管理相关参数",
            ValidValues.FLASH_DRIVER_SECTION: "# 配置 FlashDriver 相关参数",
            ValidValues.CUSTOM_DID_SECTION: "# 配置密钥 DID 相关参数"
        }
        key_comments = {
            ValidValues.CAN_TYPE_KEY: "  # 通信类型 CAN/CANFD/LIN/Uart",
            ValidValues.BAUDRATE_KEY: "  # 波特率    CAN默认500K（baudrate = 500）CANFD默认2M（baudrate = 2000）LIN默认19200（baudrate = 19200）UART无默认，设置115200即baudrate = 115200",
            ValidValues.REQUEST_ID_KEY: "  # 诊断请求ID  目前只支持11-Bit ID",
            ValidValues.RESPONSE_ID_KEY: "  # 诊断响应ID 目前只支持11-Bit ID",
            ValidValues.GET_KEY_STATUS_KEY: " # 获取秘钥状态DID",
            ValidValues.READ_WRITE_KEY_KEY: " # 读写DID",
            ValidValues.QI_TRANSMIT_ID_KEY: "  # 新增 Qi证书下载:透传发送id",
            ValidValues.QI_RECEIVE_ID_KEY: " # 新增 Qi证书下载:透传接收id",
            ValidValues.GET_QI_STATUS_KEY: "  # 新增 获取Qi秘钥状态DID",
            ValidValues.NM_ENABLED_KEY: "  # 使能网络管理报文 false不使能/true使能",
            ValidValues.NM_DLC_KEY: "  # 网络管理报文DLC，8为8字节，15为64字节",
            ValidValues.NM_ID_KEY: "  # 网络管理报文ID 目前只支持11-Bit ID",
            ValidValues.NM_PERIOD_KEY: "  # 网络管理报文周期 单位ms",
            ValidValues.NM_MESSAGE_KEY: '# 网络管理报文 64Byte十六进制字符串，小于10前面补0',
            ValidValues.FLASH_DRIVER_NAME_KEY: "  # FlashDriver文件名称"
        }
        
        # 指定需要移除引号的 key
        keys_to_remove_quotes = [
            ValidValues.REQUEST_ID_KEY, ValidValues.RESPONSE_ID_KEY, 
            ValidValues.GET_KEY_STATUS_KEY, ValidValues.READ_WRITE_KEY_KEY, 
            ValidValues.QI_TRANSMIT_ID_KEY, ValidValues.QI_RECEIVE_ID_KEY, 
            ValidValues.GET_QI_STATUS_KEY, ValidValues.NM_ID_KEY,
            # custom_did 的所有 DID
            ValidValues.GET_UID_DID_KEY, ValidValues.HUAWEI_READ_DID_KEY,
            ValidValues.HUAWEI_WRITE_DID_KEY, ValidValues.XIAOMI_READ_DID_KEY,
            ValidValues.XIAOMI_WRITE_DID_KEY, ValidValues.HONOR_READ_DID_KEY,
            ValidValues.HONOR_WRITE_DID_KEY, ValidValues.QI_READ_DID_KEY,
            ValidValues.QI_WRITE_DID_KEY, ValidValues.OPPO_READ_DID_KEY,
            ValidValues.OPPO_WRITE_DID_KEY, ValidValues.LUXQI_READ_DID_KEY,
            ValidValues.LUXQI_WRITE_DID_KEY, ValidValues.VIVO_READ_DID_KEY,
            ValidValues.VIVO_WRITE_DID_KEY,
        ]

        def remove_quotes(line, key):
            if key in keys_to_remove_quotes:
                parts = line.split("=", 1)
                if len(parts) == 2:
                    value = parts[1].strip()
                    if value.startswith(('"', "'")) and value.endswith(('"', "'")):
                        value = value[1:-1]
                    return f"{parts[0].strip()} = {value}"
            return line

        updated_lines = []
        for line in toml_lines:
            if line.startswith("[") and line.endswith("]"):
                section = line.strip("[]")
                if section in section_comments:
                    updated_lines.append(section_comments[section])
                updated_lines.append(line)
            elif "=" in line:
                key = line.split("=")[0].strip()
                line = remove_quotes(line, key)  # 调用函数移除引号
                if key in key_comments:
                    if key == ValidValues.NM_MESSAGE_KEY:
                        # 处理多行字符串的情况
                        nm_message = config[ValidValues.NM_CONFIG_SECTION][ValidValues.NM_MESSAGE_KEY]
                        updated_lines.append(f'{key} = """')
                        updated_lines.extend(nm_message.split('\n'))
                        updated_lines.append('"""')
                        updated_lines.append(key_comments[key])
                    else:
                        updated_lines.append(line + key_comments[key])
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(updated_lines) + "\n")

    def _get_config_from_ui(self):
        """从 UI 获取配置数据"""
        # 获取波特率输入，若为空则使用默认值 500
        baudrate_text = self.ui.baudrateComboBox.currentText()
        baudrate = int(baudrate_text) if baudrate_text else 500

        # 获取网络管理周期输入
        nm_period_text = self.ui.NMPeriodLineEdit.text()
        if not nm_period_text:
            nm_period = 100
            self.ui.NMPeriodLineEdit.setText("100")
        else:
            nm_period = int(nm_period_text)
            if nm_period > 65535:
                nm_period = 100
                self.ui.NMPeriodLineEdit.setText("100")
        
        # 定义函数处理十六进制输入
        def handle_hex_input(text):
            """处理标准 DID 输入，空或 0x 返回 0x0"""
            if text in ['0x', '']:
                return '0x0'
            return text
        
        def handle_custom_did_input(text):
            """处理 custom_did 的 DID 输入，无效值返回 0x0000"""
            # 去掉 0x 前缀
            hex_part = text[2:] if text.startswith('0x') else text
            # 检查是否为 1-4 个十六进制字符
            if len(hex_part) >= 1 and len(hex_part) <= 4 and all(c in '0123456789ABCDEFabcdef' for c in hex_part):
                # 补前导 0 到 4 位
                return '0x' + hex_part.upper().zfill(4)
            return '0x0000'
        
        config = {
            ValidValues.CAN_CONFIG_SECTION: {
                ValidValues.CAN_TYPE_KEY: self.ui.typeComboBox.currentText(),
                ValidValues.BAUDRATE_KEY: baudrate,
                ValidValues.REQUEST_ID_KEY: handle_hex_input(self.ui.requestIDlineEdit.text()),
                ValidValues.RESPONSE_ID_KEY: handle_hex_input(self.ui.responseIDlineEdit.text())
            },
            ValidValues.DIAG_DID_SECTION: {
                ValidValues.GET_KEY_STATUS_KEY: handle_hex_input(self.ui.getKeyStatusDIDlineEdit.text()),
                ValidValues.READ_WRITE_KEY_KEY: handle_hex_input(self.ui.readWriteKeyDIDlineEdit.text())
            },
            ValidValues.QI_CERTIFICATE_SECTION: {
                ValidValues.QI_TRANSMIT_ID_KEY: handle_hex_input(self.ui.qiTransmitIDlineEdit.text()),
                ValidValues.QI_RECEIVE_ID_KEY: handle_hex_input(self.ui.qiReceiveIDlineEdit.text()),
                ValidValues.GET_QI_STATUS_KEY: handle_hex_input(self.ui.getQiStatusDIDlineEdit.text())
            },
            ValidValues.NM_CONFIG_SECTION: {
                ValidValues.NM_ENABLED_KEY: self.ui.nmEnabledCheckBox.isChecked(),
                ValidValues.NM_DLC_KEY: self.ui.NMDLCcomboBox.currentIndex(),
                ValidValues.NM_ID_KEY: handle_hex_input(self.ui.NMIDlineEdit.text()),
                ValidValues.NM_PERIOD_KEY: nm_period,
                ValidValues.NM_MESSAGE_KEY: self._get_nm_message_from_table()
            }
        }
        
        # 只有 FlashDriver_name 不为空时才添加 FlashDriver 配置组
        flash_driver_name = self.ui.FlashDriverNameLineEdit.text().strip()
        if flash_driver_name:
            config[ValidValues.FLASH_DRIVER_SECTION] = {
                ValidValues.FLASH_DRIVER_NAME_KEY: flash_driver_name
            }
        
        # 如果勾选了 cusdomKeyDIDcheckBox，保存 custom_did 配置
        if self.ui.cusdomKeyDIDcheckBox.isChecked():
            config[ValidValues.CUSTOM_DID_SECTION] = {
                ValidValues.GET_UID_DID_KEY: handle_custom_did_input(self.ui.getUIDDIDlineEdit.text()),
                ValidValues.HUAWEI_READ_DID_KEY: handle_custom_did_input(self.ui.readHuaweiDIDlineEdit.text()),
                ValidValues.HUAWEI_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeHuaweiDIDlineEdit.text()),
                ValidValues.XIAOMI_READ_DID_KEY: handle_custom_did_input(self.ui.readXiaomiKeyDIDlineEdit.text()),
                ValidValues.XIAOMI_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeXiaomiKeyDIDlineEdit.text()),
                ValidValues.HONOR_READ_DID_KEY: handle_custom_did_input(self.ui.readHonorKeyDIDlineEdit.text()),
                ValidValues.HONOR_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeHonorKeyDIDlineEdit.text()),
                ValidValues.QI_READ_DID_KEY: handle_custom_did_input(self.ui.readQiDIDlineEdit.text()),
                ValidValues.QI_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeQiDIDlineEdit.text()),
                ValidValues.OPPO_READ_DID_KEY: handle_custom_did_input(self.ui.readOppoKeyDIDlineEdit.text()),
                ValidValues.OPPO_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeOppoKeyDIDlineEdit.text()),
                ValidValues.LUXQI_READ_DID_KEY: handle_custom_did_input(self.ui.readLuxQiDIDlineEdit.text()),
                ValidValues.LUXQI_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeLuxQiDIDlineEdit.text()),
                ValidValues.VIVO_READ_DID_KEY: handle_custom_did_input(self.ui.readVivoKeyDIDlineEdit.text()),
                ValidValues.VIVO_WRITE_DID_KEY: handle_custom_did_input(self.ui.writeVivoKeyDIDlineEdit.text()),
            }
        
        return config

    def _get_nm_message_from_table(self):
        """从表格获取网络管理报文"""
        nm_message = []
        for row in range(8):
            for col in range(8):
                item = self.ui.NMDataTableWidget.item(row, col)
                if item:
                    # 检查单元格是否可编辑
                    if item.flags() & Qt.ItemIsEditable:
                        nm_message.append(item.text())
        return '\n'.join([' '.join(nm_message[i:i+8]) for i in range(0, len(nm_message), 8)])

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

    def _on_cusdom_key_did_checkbox_changed(self, state):
        """
        处理 cusdomKeyDIDcheckBox 状态变化
        - 勾选时：readWriteKeyDIDlineEdit 和 getQiStatusDIDlineEdit 为 disable，keyDIDWidget 保持可见
        - 不勾选时：readWriteKeyDIDlineEdit 和 getQiStatusDIDlineEdit 为 enable，keyDIDWidget 为不可见，清空 custom_did 输入
        - 勾选时：高度至少 850
        - 不勾选时：高度最多 700
        """
        is_checked = bool(state)
        
        # 设置 readWriteKeyDIDlineEdit 和 getQiStatusDIDlineEdit 的启用状态
        self.ui.readWriteKeyDIDlineEdit.setEnabled(not is_checked)
        self.ui.getQiStatusDIDlineEdit.setEnabled(not is_checked)
        
        # 设置 keyDIDWidget 的可见性（不勾选时隐藏）
        self.ui.keyDIDWidget.setVisible(is_checked)
        
        # 取消勾选时清空所有 custom_did 的 lineEdit，显示 0x 提示
        if not is_checked:
            self.ui.getUIDDIDlineEdit.setText('0x')
            self.ui.readHuaweiDIDlineEdit.setText('0x')
            self.ui.writeHuaweiDIDlineEdit.setText('0x')
            self.ui.readXiaomiKeyDIDlineEdit.setText('0x')
            self.ui.writeXiaomiKeyDIDlineEdit.setText('0x')
            self.ui.readHonorKeyDIDlineEdit.setText('0x')
            self.ui.writeHonorKeyDIDlineEdit.setText('0x')
            self.ui.readQiDIDlineEdit.setText('0x')
            self.ui.writeQiDIDlineEdit.setText('0x')
            self.ui.readOppoKeyDIDlineEdit.setText('0x')
            self.ui.writeOppoKeyDIDlineEdit.setText('0x')
            self.ui.readLuxQiDIDlineEdit.setText('0x')
            self.ui.writeLuxQiDIDlineEdit.setText('0x')
            self.ui.readVivoKeyDIDlineEdit.setText('0x')
            self.ui.writeVivoKeyDIDlineEdit.setText('0x')
        
        # 获取当前尺寸
        current_width = self.width()
        current_height = self.height()
        print(f"[调试] 勾选状态变化前 - 宽度: {current_width}, 高度: {current_height}")
        
        if is_checked:
            # 勾选时：显示 keyDIDWidget，高度至少 850
            new_height = max(850, current_height + 150)
        else:
            # 不勾选时：隐藏 keyDIDWidget，高度最多 700
            new_height = max(700, current_height - 150)
        
        # 固定宽度，只调整高度
        self.resize(current_width, new_height)
        
        # 打印调整后的尺寸
        final_width = self.width()
        final_height = self.height()
        print(f"[调试] 勾选状态变化后 - 宽度: {final_width}, 高度: {final_height}, keyDIDWidget可见: {self.ui.keyDIDWidget.isVisible()}")

    def closeEvent(self, event):
        """重写关闭事件"""
        self.closed.emit()  # 发出关闭信号
        event.accept()

