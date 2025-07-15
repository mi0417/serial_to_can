
"""
"""
import os
import logging
from io import StringIO
from datetime import datetime
import toml

from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QStyledItemDelegate, QLineEdit, QHeaderView, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon, QRegularExpressionValidator, QShortcut, QKeySequence
from PySide6.QtCore import Signal, Qt, QRegularExpression

from panel.config_edit_ui import Ui_configEditWindow
from utils.file_utils import resource_path, read_toml_file
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
            self.ui.NMIDlineEdit: [3, 4]            # [3,4,7]
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

    def _connect_file_actions(self):
        """连接文件操作信号"""
        self.ui.importAction.triggered.connect(self.import_config)
        self.ui.saveAction.triggered.connect(self.save_config)
        self.ui.saveAsAction.triggered.connect(self.save_as_config)

    def import_config(self):
        """点击导入键导入配置文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "导入配置文件", "", "TOML 文件 (*.toml)")
        if file_path:
            self.is_import_button_clicked = True  # 设置标志位
            self.load_config_file(file_path)
            self.is_import_button_clicked = False  # 重置标志位

    def load_config_file(self, file_path):
        """加载配置文件内容并填充 UI"""
        # 检查文件是否存在
        if not os.path.exists(file_path):
            error_msg = f"配置文件 {file_path} 不存在"
            logger.error(error_msg)
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

            baudrate = can_config.get('baudrate', 0)
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

        logger.debug("填充配置到界面完成，日志信息: %s", fill_log)
        return fill_log
            
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
            "CAN_config": "# 配置 CAN 通信相关参数",
            "diag_did": "# 配置诊断 DID 相关参数",
            "Qi_certificate": "# 配置 Qi 证书相关参数",
            "nm_config": "# 配置网络管理相关参数"
        }
        key_comments = {
            "type": "  # 通信类型 CAN/CANFD/LIN/Uart",
            "baudrate": "  # 波特率    CAN默认500K（baudrate = 500）CANFD默认2M（baudrate = 2000）LIN默认19200（baudrate = 19200）UART无默认，设置115200即baudrate = 115200",
            "request_id": "  # 诊断请求ID  目前只支持11-Bit ID",
            "response_id": "  # 诊断响应ID 目前只支持11-Bit ID",
            "get_key_status": " # 获取秘钥状态DID",
            "read_write_key": " # 读写DID",
            "qi_transmit_id": "  # 新增 Qi证书下载:透传发送id",
            "qi_receive_id": " # 新增 Qi证书下载:透传接收id",
            "get_qi_status": "  # 新增 获取Qi秘钥状态DID",
            "nm_enabled": "  # 使能网络管理报文 false不使能/true使能",
            "nm_DLC": "  # 网络管理报文DLC，8为8字节，15为64字节",
            "nm_id": "  # 网络管理报文ID 目前只支持11-Bit ID",
            "nm_period": "  # 网络管理报文周期 单位ms",
            "nm_message": '# 网络管理报文 64Byte十六进制字符串，小于10前面补0'
        }
        
        # 指定需要移除引号的 key
        keys_to_remove_quotes = ["request_id", "response_id", "get_key_status", "read_write_key", "qi_transmit_id", "qi_receive_id", "get_qi_status", "nm_id"]

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
                    if key == "nm_message":
                        # 处理多行字符串的情况
                        nm_message = config['nm_config']['nm_message']
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
        
        # 定义一个函数处理十六进制输入
        def handle_hex_input(text):
            if text in ['0x', '']:
                return '0x0'
            return text
        
        config = {
            'CAN_config': {
                'type': self.ui.typeComboBox.currentText(),
                'baudrate': baudrate,
                'request_id': handle_hex_input(self.ui.requestIDlineEdit.text()),
                'response_id': handle_hex_input(self.ui.responseIDlineEdit.text())
            },
            'diag_did': {
                'get_key_status': handle_hex_input(self.ui.getKeyStatusDIDlineEdit.text()),
                'read_write_key': handle_hex_input(self.ui.readWriteKeyDIDlineEdit.text())
            },
            'Qi_certificate': {
                'qi_transmit_id': handle_hex_input(self.ui.qiTransmitIDlineEdit.text()),
                'qi_receive_id': handle_hex_input(self.ui.qiReceiveIDlineEdit.text()),
                'get_qi_status': handle_hex_input(self.ui.getQiStatusDIDlineEdit.text())
            },
            'nm_config': {
                'nm_enabled': self.ui.nmEnabledCheckBox.isChecked(),
                'nm_DLC': self.ui.NMDLCcomboBox.currentIndex(),
                'nm_id': handle_hex_input(self.ui.NMIDlineEdit.text()),
                'nm_period': nm_period,
                'nm_message': self._get_nm_message_from_table()
            }
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

    def closeEvent(self, event):
        """重写关闭事件"""
        self.closed.emit()  # 发出关闭信号
        event.accept()

