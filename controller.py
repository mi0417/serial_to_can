
import time
import logging
import queue
import serial
from PySide6.QtCore import QObject, Signal, QThread, QThreadPool, QRunnable, QTimer

from model import SerialModel
from view.view import View

from utils.data_processor import ConfigParams, ValidValues
from utils.file_utils import exe_absolute_path, is_file_exists
from utils.common_data_utils import array_to_ascii, byte_array_to_hex_string, format_timestamp

logger = logging.getLogger(__name__)

class SerialCommunicationThread(QThread):
    '''
    自定义线程类，用于打开串口并接收数据
    '''
    EMIT_STR_ERROR = 'error'
    data_received = Signal(object, str, str)
    result_signal = Signal(bool, str)  # 自定义信号，用于传递打开串口的结果给主线程
    sw_ver_signal = Signal(str)  # 自定义信号，用于传递软件版本号给主线程
    serial_closed_signal = Signal(bool, str)  # 自定义信号，用于通知界面串口已关闭 True表示主动关闭
    reset_result_signal = Signal(bool, str)  # 自定义信号，用于传递复位结果给主线程
    set_config_result_signal = Signal(bool, str)  # 自定义信号，用于传递配置结果给主线程
    read_config_result_signal = Signal(str, str)  # 自定义信号，用于传递读取配置结果给主线程
    get_key_status_result_signal = Signal(list, str)  # 自定义信号，用于传递获取密钥状态结果给主线程

    # 请求队列
    _request_queue = queue.Queue()

    def __init__(self, model: SerialModel, port_name, baudrate, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=1, toml_path = 'tool-config.toml', data_queue=None):
        super().__init__()
        logger.debug('创建串口子线程 %s', self)
        self.model = model
        self.port_name = port_name
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.timeout = timeout
        self.toml_path = toml_path
        self.set_toml_path()
        self._running = True
        self.data_queue = data_queue
        self._current_request = None  # 当前请求状态跟踪
        self._is_processing = False  # 处理状态标志

    def run(self):
        logger.debug('串口子线程run %s', self)
        # 尝试打开串口
        result = self.model.open_serial_port(self.port_name, self.baudrate, self.bytesize, self.stopbits, self.timeout)
        self.result_signal.emit(result, self.port_name)

        if result:
            # 串口打开成功，读取软件版本号
            self.get_software_version()
            dynamic_sleep = 0.01  # 初始间隔
            # 开始接收数据
            while self._running and self.model.is_serial_open():
                try:
                    # 处理数据前检查队列深度
                    queue_depth = self._request_queue.qsize()
                    
                    # 动态调整睡眠时间
                    if queue_depth > 3:
                        dynamic_sleep = 0.001  # 高负载时快速响应
                    elif queue_depth > 0:
                        dynamic_sleep = 0.01   # 中等负载
                    else:
                        dynamic_sleep = 0.03   # 空闲时降低CPU占用

                    # 请求处理逻辑
                    if not self._is_processing and not self._request_queue.empty():
                        req = self._request_queue.get()
                        self._is_processing = True
                        self._current_request = req
                        # 分离耗时操作到工作线程
                        self.start_async_request(req)  # 异步处理方法

                    receive_data = self.model.get_received_data()
                    for data in receive_data:
                        # logger.debug("%s",receive_data)
                        self.data_received.emit((format_timestamp(data['timestamp']), data['data']), View.LOG_RECEIVE, View.HEX)

                    # 获取已发送指令并处理
                    sent_commands = self.model.get_sent_commands()
                    for cmd in sent_commands:
                        # logger.debug("%s:%s",format_timestamp(cmd['timestamp']), cmd['data'])
                        # hex_data = byte_array_to_hex_string(cmd['data'])
                        # status = f"重试 ({cmd['retry']}/{cmd['max_retries']}) {hex_data}"
                        self.data_received.emit((format_timestamp(cmd['timestamp']), cmd['data']), View.LOG_SEND, View.HEX)
                    
                    # 仅在非主动请求时处理常规接收
                    if not self.model.expect_response:
                        # 接收数据（receive_data从串口接收数据，没有这一步log_data获取不到缓冲区数据），根据类型emit，无对应类型则输出信息
                        message = self.model.receive_data()
                        # 定时获取日志缓冲区（ASCII格式）
                        log_data = self.model.get_realtime_logs()
                        if log_data:
                            self.data_received.emit(log_data, View.LOG_RECEIVE, View.ASCII)
                    # pass
                except Exception as e:
                    logger.error('Error receiving data from serial: %s', e)
                time.sleep(dynamic_sleep)
            if self._running and not self.model.is_serial_open():
                self.serial_closed_signal.emit(False, self.port_name)  # 发送串口关闭信号

    

    # 异步处理方法
    def start_async_request(self, req):
        req_method = getattr(self.model, req['method'])
        class RequestWorker(QRunnable):
            def __init__(self, method, args, callback, outer):
                super().__init__()
                self.method = method
                # self.args = args
                self.args = args if isinstance(args, (list, tuple)) else [args]
                self.callback = callback
                self.outer = outer  # 外部类引用

            def run(self):
                try:
                    result = self.method(*self.args)
                    self.callback(result)
                except Exception as e:
                    logger.error(f"异步请求执行失败: {e}")
                finally:
                    self.outer._is_processing = False  # 无论成功失败都重置状态
                    self.outer._current_request = None

        worker_args = req.get('args', []) or []  # 确保空值时转为空列表
        worker = RequestWorker(
            req_method, 
            # req.get('args', []), 
            worker_args,
            req['callback'],
            self  # 外部类引用
        )
        QThreadPool.globalInstance().start(worker)

    def get_software_version(self):
        '''
        获取软件版本号
        '''
        def _callback(result):
            if result:
                self.sw_ver_signal.emit(result)
            else:
                self.sw_ver_signal.emit(self.EMIT_STR_ERROR)
        self._request_queue.put({
            'method': 'get_software_version',
            'callback': _callback
        })
        # software_version = self.model.get_software_version()
        # if software_version:
        #     self.sw_ver_signal.emit(software_version)
        # else:
        #     self.sw_ver_signal.emit(self.EMIT_STR_ERROR)

    def reset_device(self):
        '''
        复位设备
        '''
        def _callback(result):
            self.reset_result_signal.emit(result, self.port_name)

        self._request_queue.put({
            'method': 'reset_device',
            'callback': _callback
        })
        # result = self.model.reset_device()
        # self.reset_result_signal.emit(result, self.port_name)
        # return result

    def set_config_device(self, toml_path=None):
        '''
        配置设备
        1、复位设备
        2、配置设备
        3、读取设备配置并确认
        '''
        if not toml_path:
            toml_path = self.toml_path
        else:
            toml_path = exe_absolute_path(toml_path)

        if not is_file_exists(toml_path):
            self.set_config_result_signal.emit(None, ConfigParams.PATH_ERROR)
            return

        # 定义配置完成的回调
        def config_callback(result):
            self.set_config_result_signal.emit(result[0], result[1])

        # 定义复位完成的回调
        def reset_callback(result):
            if result:
                time.sleep(0.5)     # 复位后发送配置延时
                self._request_queue.put({
                    'method': 'config_device',
                    'args': [toml_path],
                    'callback': config_callback
                })
            else:
                self.set_config_result_signal.emit(False, '复位失败，未执行配置')

        # 将复位请求加入队列
        self._request_queue.put({
            'method': 'reset_device',
            'callback': reset_callback
        })
        # result = self.model.reset_device()
        # if result:
        # # if self.reset_device():

        #     result, message = self.model.config_device(toml_path)
        #     self.set_config_result_signal.emit(result, message)
        # else:
        #     self.set_config_result_signal.emit(False, '复位失败，未执行配置')

    def read_config_device(self):
        '''
        读取设备配置
        '''
        def _callback(result):
            if result is not None and result[0] is None and result[1] is None:
                self.read_config_result_signal.emit(None, '读取失败')
            else:
                self.read_config_result_signal.emit(result[0], result[1])
        
        self._request_queue.put({
            'method': 'read_device_config',
            'callback': _callback
        })
        # result, message = self.model.read_device_config()
        # if not result and not message:
        #     self.read_config_result_signal.emit(result, '读取失败')
        # else:
        #     self.read_config_result_signal.emit(result, message)
    
    def get_key_status(self):
        '''
        获取密钥状态
        '''
        def _callback(result):
            if result is not None and result[0] is None and result[1] is None:
                self.get_key_status_result_signal.emit(None, '读取失败')
            else:
                self.get_key_status_result_signal.emit(result[0], result[1])
        
        self._request_queue.put({
            'method': 'get_key_status',
            'callback': _callback
        })
        # result, message = self.model.get_key_status()
        # if not result and not message:
        #     self.get_key_status_result_signal.emit(result, '读取失败')
        # self.get_key_status_result_signal.emit(result, message)


    # def receive_data(self):

    def send_data(self, data):
        '''
        发送数据到串口
        :param data: 要发送的数据
        '''
        try:
            if self.model.is_serial_open():
                self.model.send_request_with_retry(data)
        except Exception as e:
            logger.error('Error sending data to serial: %s', e)
            if not self.model.is_serial_open():  # 检查串口是否关闭
                self.serial_closed_signal.emit(False, self.port_name)  # 发送串口关闭信号

    def set_toml_path(self):
        self.toml_path = exe_absolute_path(self.toml_path)
    
    def restart(self, port_name):
        if self.isRunning():
            self.stop()
            self.wait()  # 等待线程结束
        self._running = True
        self.port_name = port_name
        self.start()
        logger.debug('串口子线程restart %s', self)

    def stop(self):
        self._running = False
        self.model.close_serial_port()  # 关闭串口
        self.serial_closed_signal.emit(True, self.port_name)  # 发送串口关闭信号

    def __del__(self):
        logger.debug('串口子线程被销毁 %s', self)    

class Controller(QObject):
    def __init__(self, icon_path=None, window_title=None):
        super().__init__()  # 调用父类的构造函数
        logger.debug('程序开始运行')
        logger.debug('Controller ID in SerialController: %s', id(self))
        self.model = SerialModel()
        self.view = View(icon_path, window_title)
        self.view.controller = self
        self.setup_connections()
        self.serial_thread = None  # 存储单个串口通信线程
        self.data_queue = queue.Queue()  # 用于存储接收到的数据
        self.one_key_config_running = False  # 用于跟踪一次配置过程是否正在运行

    def setup_connections(self):
        # 这里可以设置用户交互的连接，例如按钮点击事件
        self.view.ui.connectButton.clicked.connect(self.toggle_serial)
        self.view.ui.getSwVerButton.clicked.connect(self.get_software_version)
        self.view.ui.resetButton.clicked.connect(self.reset_device)
        self.view.ui.setConfigButton.clicked.connect(self.set_config_device)
        self.view.ui.getConfigButton.clicked.connect(self.read_config_device)
        self.view.ui.oneKeyButton.clicked.connect(self.one_key_config)
        self.view.ui.getKeyStatusButton.clicked.connect(self.get_key_status)

    def toggle_serial(self):
        port = self.view.ui.serialBox.currentText()
        port_name = port.split(' #')[0]
        if not port_name:
            logger.error('未选择串口')
            return

        if self.serial_thread and self.serial_thread.isRunning():
            # 如果线程正在运行，关闭串口
            self.serial_thread.stop()
            self.serial_thread.wait()
            self.view.ui.connectButton.setText(View.BTN_CONNECT)
            self.view.write_to_statusbar(f'已关闭串口 {port_name}')
            self.view.append_to_output_widget(f'已关闭串口 {port_name}', self.view.LOG_TYPE_INFO)
            self.view.append_to_log_edit('串口关闭', None, None, None)
            logger.info('已关闭串口 %s', port_name)
            # 串口断开后，设置下拉框可编辑
            self.view.ui.serialBox.setEnabled(True)
        else:
            # 如果线程未运行，打开串口
            baudrate = 115200
            timeout = 1
            if self.serial_thread is None:
                self.serial_thread = SerialCommunicationThread(self.model, port_name, baudrate=baudrate, timeout=timeout, data_queue=self.data_queue)
                self.serial_thread.result_signal.connect(self.handle_serial_open_result)
                self.serial_thread.data_received.connect(self.handle_received_data) # 接收数据
                self.serial_thread.sw_ver_signal.connect(self.handle_received_sw_version)
                self.serial_thread.serial_closed_signal.connect(self.handle_serial_closed)
                self.serial_thread.reset_result_signal.connect(self.handle_reset_result)
                self.serial_thread.set_config_result_signal.connect(self.handle_set_config_result)
                self.serial_thread.read_config_result_signal.connect(self.handle_read_config_result)
                self.serial_thread.get_key_status_result_signal.connect(self.handle_get_key_status_result)
            self.serial_thread.restart(port_name)
            # 串口连接后，设置下拉框不可编辑
            self.view.ui.serialBox.setEnabled(False)

    def handle_serial_open_result(self, result, port:str):
        port_name = port.split(' #')[0]
        if result:
            self.view.ui.connectButton.setText(View.BTN_DISCONNECT)
            # 串口连接后，设置下拉框不可编辑
            self.view.ui.serialBox.setEnabled(False)
            logger.info('成功打开串口 %s', self.model.serial.port)
            self.view.write_to_statusbar(f'成功打开串口 {self.model.serial.port}')
            self.view.append_to_output_widget(f'成功打开串口 {self.model.serial.port}', self.view.LOG_TYPE_INFO)
            self.view.append_to_log_edit('打开串口', None, None, None)
            self.view.enable_operation_buttons()
        else:
            logger.error('无法打开串口 %s', port_name)
            self.view.ui.connectButton.setText(View.BTN_CONNECT)
            self.view.write_to_statusbar(f'无法打开串口 {port_name}', True)
            # 串口断开后，设置下拉框可编辑
            self.view.ui.serialBox.setEnabled(True)
            self.view.enable_operation_buttons()

    def handle_serial_closed(self, close_status, port:str):
        '''
        处理串口关闭信号
        :param close_status: 串口关闭状态，True表示主动关闭，False表示被动关闭
        :param port_name: 串口名称
        '''
        
        port_name = port.split(' #')[0]
        if not close_status and self.view.ui.connectButton.text() == View.BTN_DISCONNECT:
            self.view.ui.connectButton.setText(View.BTN_CONNECT)
            self.view.write_to_statusbar(f'串口 {port_name} 已断开')
            self.view.append_to_output_widget(f'串口 {port_name} 已断开', self.view.LOG_TYPE_INFO)
            self.view.append_to_log_edit('串口断开', None, None, None)
            logger.info('串口 %s 已断开', port_name)
            # 串口断开后，设置下拉框可编辑
            self.view.ui.serialBox.setEnabled(True)
            self.view.enable_operation_buttons()

    def get_software_version(self):
        '''
        获取软件版本号
        '''
        logger.info('点击获取软件版本号按钮')
        if self.serial_thread and self.serial_thread.isRunning():
            self.view.append_to_output_widget(self.view.ui.getSwVerButton.text(), self.view.LOG_TYPE_INFO)
            self.serial_thread.get_software_version()
            self.view.disable_operation_buttons()
        else:
            self.view.append_to_output_widget('串口未打开', self.view.LOG_TYPE_ERROR)
            logger.error('串口未打开')

    def handle_received_sw_version(self, version):
        if version !=SerialCommunicationThread.EMIT_STR_ERROR:
            self.view.ui.swVerLabel.setText(version)
            self.view.append_to_output_widget(f'软件版本号 {version}', self.view.LOG_TYPE_DATA)
            self.view.change_label_text(self.view.ui.swVerLabel, version)
        else:
            self.view.ui.swVerLabel.setText('获取软件版本号失败')
            self.view.append_to_output_widget('获取软件版本号失败', self.view.LOG_TYPE_ERROR)
        self.view.enable_operation_buttons()

    def reset_device(self):
        '''
        复位设备
        '''
        logger.info('点击复位按钮')
        if self.serial_thread and self.serial_thread.isRunning():
            self.view.append_to_output_widget(self.view.ui.resetButton.text(), self.view.LOG_TYPE_INFO)
            self.serial_thread.reset_device()
            self.view.disable_operation_buttons()
        else:
            self.view.append_to_output_widget('串口未打开', self.view.LOG_TYPE_ERROR)
            logger.error('串口未打开')

    def handle_reset_result(self, result, port_name):
        '''
        处理复位结果信号
        :param result: 复位结果，True表示成功，False表示失败
        '''
        if result:
            self.view.append_to_output_widget(f'复位成功', self.view.LOG_TYPE_INFO)
        else:
            self.view.append_to_output_widget(f'复位失败', self.view.LOG_TYPE_ERROR)
        self.view.enable_operation_buttons()

    def check_config_file(self):
        '''
        检查配置文件是否存在
        '''
        if not is_file_exists(self.view.config_path):
            self.view.append_to_output_widget(f'配置文件不存在{self.view.config_path}', self.view.LOG_TYPE_ERROR)
            logger.error('配置文件不存在%s', self.view.config_path)
            return False
        return True

    def set_config_device(self):
        '''
        配置设备
        '''
        logger.info('点击配置按钮')
        check_config_file_result = self.check_config_file()
        if not check_config_file_result:
            return
        toml_path=self.view.config_path
        if self.serial_thread and self.serial_thread.isRunning():
            # 先断开旧信号连接
            try:
                self.serial_thread.set_config_result_signal.disconnect()
            except Exception:
                pass    
            # 重新连接信号
            self.serial_thread.set_config_result_signal.connect(self.handle_set_config_result)
        
            self.view.append_to_output_widget(self.view.ui.setConfigButton.text(), self.view.LOG_TYPE_INFO)
            self.serial_thread.set_config_device(toml_path)
            self.view.disable_operation_buttons()
        else:
            self.view.append_to_output_widget('串口未打开', self.view.LOG_TYPE_ERROR)
            logger.error('串口未打开')

    def handle_set_config_result(self, result, message):
        '''
        处理配置结果信号
        :param result: 配置结果，True表示成功，False表示失败
        '''
        if result:
            self.view.append_to_output_widget(f'配置成功', self.view.LOG_TYPE_INFO)
            if not self.one_key_config_running:  # 检查是否正在进行一次配置
                self.view.enable_operation_buttons()
        else:
            if message == ConfigParams.PATH_ERROR:
                self.view.append_to_output_widget(f'配置失败，找不到配置文件{self.serial_thread.toml_path}', self.view.LOG_TYPE_ERROR)
            elif message == ConfigParams.PARAM_NOT_FOUND_ERROR:
                self.view.append_to_output_widget(f'配置失败，缺少配置参数', self.view.LOG_TYPE_ERROR)
            elif message == ConfigParams.CONFIG_PARAMS_ERROR:
                self.view.append_to_output_widget(f'配置失败，配置参数错误', self.view.LOG_TYPE_ERROR)
            else:
                self.view.append_to_output_widget(f'配置失败，{message}', self.view.LOG_TYPE_ERROR)
            self.view.enable_operation_buttons()

    def read_config_device(self):
        '''
        读取设备配置
        '''
        logger.info('点击读取配置按钮')
        if self.serial_thread and self.serial_thread.isRunning():
            self.view.append_to_output_widget(self.view.ui.getConfigButton.text(), self.view.LOG_TYPE_INFO)
            self.serial_thread.read_config_device()
            self.view.disable_operation_buttons()
        else:
            self.view.append_to_output_widget('串口未打开', self.view.LOG_TYPE_ERROR)
            logger.error('串口未打开')

    def handle_read_config_result(self, result, message):
        '''
        处理读取配置结果信号
        :param result: 读取到的配置
        :param message: 错误信息
        '''
        if result:
            self.view.append_to_output_widget(f'读取配置成功', self.view.LOG_TYPE_INFO)
            self.view.append_to_output_widget(f'配置信息\n{result}', self.view.LOG_TYPE_DATA)
        else:
            self.view.append_to_output_widget(f'读取配置失败, {message}', self.view.LOG_TYPE_ERROR)
        self.one_key_config_running = False
        self.view.enable_operation_buttons()

    def one_key_config(self):
        '''
        一键配置
        '''
        logger.info('点击一键配置按钮')
        check_config_file_result = self.check_config_file()
        if not check_config_file_result:
            return
        if self.serial_thread and self.serial_thread.isRunning():
            self.one_key_config_running = True
            self.view.disable_operation_buttons()

            self.view.append_to_output_widget(self.view.ui.oneKeyButton.text(), self.view.LOG_TYPE_INFO)
            
            def after_config(result, message):
                if result:
                    self.serial_thread.read_config_device()
                else:
                    self.one_key_config_running = False
                # 处理完成后断开信号连接
                self.serial_thread.set_config_result_signal.disconnect(after_config_wrapper)

        
            # 包装器函数用于参数匹配
            after_config_wrapper = lambda result, message: after_config(result, message)
            
            # 连接信号到中间层
            self.serial_thread.set_config_result_signal.connect(after_config_wrapper)
      
            # 开始配置流程
            self.serial_thread.set_config_device(self.view.config_path)
            # self.serial_thread.get_software_version()
            # self.serial_thread.set_config_device(self.view.config_path)
            # self.serial_thread.read_config_device()
        else:
            self.view.append_to_output_widget('串口未打开', self.view.LOG_TYPE_ERROR)
            logger.error('串口未打开')

    def get_key_status(self):
        '''
        获取密钥状态
        '''
        logger.info('点击获取密钥状态按钮')
        if self.serial_thread and self.serial_thread.isRunning():
            self.view.append_to_output_widget(self.view.ui.getKeyStatusButton.text(), self.view.LOG_TYPE_INFO)
            self.serial_thread.get_key_status()
            self.view.disable_operation_buttons()
        else:
            self.view.append_to_output_widget('串口未打开', self.view.LOG_TYPE_ERROR)
            logger.error('串口未打开')

    def handle_get_key_status_result(self, key_status_list, message):
        '''
        处理获取密钥状态结果信号
        :param result: 密钥状态列表
        :param message: 错误信息
        '''
        if key_status_list:
            
            try:
                self.view.append_to_output_widget(f'获取密钥状态成功', self.view.LOG_TYPE_INFO)
                device_labels = [
                    (self.view.ui.xiaomiKeyStatus, self.view.ui.xiaomiFastChargeStatus),
                    (self.view.ui.oppoKeyStatus, self.view.ui.oppoFastChargeStatus),
                    (self.view.ui.vivoKeyStatus, self.view.ui.vivoFastChargeStatus),
                    (self.view.ui.huaweiKeyStatus, self.view.ui.huaweiFastChargeStatus),
                    (self.view.ui.honorKeyStatus, self.view.ui.honorFastChargeStatus),
                    (self.view.ui.QiCertStatus, None)
                ]

                # 检查 key_status_list 和 device_labels 长度是否一致
                if len(key_status_list) != len(device_labels):
                    raise ValueError('密钥状态列表和设备标签列表长度不一致')

                for i, (download_status, enable_status) in enumerate(key_status_list):
                    key_label, charge_label = device_labels[i]
                    download_text = '下载成功' if download_status else '未下载'
                    download_color = None if download_status else View.COLOR_RED
                    self.view.change_label_text(key_label, download_text, download_color)

                    if charge_label:
                        charge_text = '开启' if enable_status else '未开启'
                        charge_color = None if enable_status else View.COLOR_RED
                        self.view.change_label_text(charge_label, charge_text, charge_color)

            except ValueError as ve:
                # 处理列表长度不一致的错误
                self.view.append_to_output_widget(f'处理密钥状态时出错: {ve}', self.view.LOG_TYPE_ERROR)
                logger.error(f'处理密钥状态时出错: {ve}')
            except Exception as e:
                # 处理其他未知错误
                self.view.append_to_output_widget(f'处理密钥状态时发生未知错误: {e}', self.view.LOG_TYPE_ERROR)
                logger.error(f'处理密钥状态时发生未知错误: {e}')

        else:
            self.view.append_to_output_widget(f'获取密钥状态失败, {message}', self.view.LOG_TYPE_ERROR)
        self.view.enable_operation_buttons()

    def handle_received_data(self, log_message, type=View.LOG_RECEIVE, decode=View.ASCII):
        '''
        处理消息并传递给View的log_to_edit方法，用于在log中显示发送和接收指令的Hex和接收到的log的ASCII
        :param message: 原始消息
        :param type: 日志类型
        :param decode: 解码方式
        '''
        # self.view.log_message(f'接收到数据：{data}', self.view.LOG_TYPE_DATA)
        # 在这里对message进行处理
        log_time = None

        if decode == View.HEX:
            try:
                log_time, message = log_message
                processed_message = byte_array_to_hex_string(message)
            except Exception as e:
                logger.error(f'Hex编码失败: {e}')
                processed_message = message
        else:
            try:
                processed_message = array_to_ascii(log_message)
            except Exception as e:
                logger.error(f'ASCII编码失败: {e}')
                processed_message = message
        
        # 调用View的log_to_edit方法
        self.view.append_to_log_edit(processed_message, log_time=log_time, type=type, decode=decode)

    def show_view(self):
        self.view.show()

    def cleanup(self):
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread.wait()
            self.serial_thread = None