'''
Model类
处理数据

'''
import time
import random
import logging
import serial
import threading
from utils.serial_handle import SerialOperator
from utils.data_processor import SerialMessage, ValidValues, ConfigParams, MIN_DATA_LENGTH
import utils.common_data_utils as utils

logger = logging.getLogger(__name__)

class SerialModel:
    def __init__(self):
        logger.debug('Serial ID in SerialModel: %s', id(self))
        self.last_receive_time = time.time()  # 初始化时间戳
        self.serial = SerialOperator()  # 只保留一个串口操作对象
        self.data_buffer = bytearray()  # 添加数据缓冲区
        self.receive_buffer = []  # 接收数据缓冲区
        self.log_buffer = bytearray()  # 独立日志缓冲区，用于显示串口log
        self.buffer_lock = threading.Lock()  # 缓冲区锁
        self.sent_buffer = []  # 已发送指令缓冲区
        self.sent_lock = threading.Lock()  # 缓冲区锁
        self.expect_response = False  # 响应期待标志位
        self.active_request_command = None  # 当前活动请求的命令类型

    def get_available_ports(self):
        '''
        获取设备上的串口
        '''
        return self.serial.list_available_ports(True)

    def open_serial_port(self, port_name, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=1):
        '''
        打开串口
        '''
        self.last_receive_time = time.time()  # 更新时间戳
        return self.serial.open_serial_port(port_name, baudrate, bytesize, stopbits, timeout)

    def close_serial_port(self):
        '''
        关闭串口
        '''
        self.serial.close_serial_port()

    def is_serial_open(self):
        '''
        返回串口打开状态
        '''
        return self.serial.is_open
    
    def get_realtime_logs(self):
        '''获取实时日志数据'''
        with self.buffer_lock:
            log_data = bytes(self.log_buffer)
            self.log_buffer.clear()  # 清空已读取的日志数据
        return log_data

    def receive_data(self):
        '''
        接收数据
        '''
        data = self.serial.receive_data()
                    
        if data:
            self.last_receive_time = time.time()  # 更新时间戳
            with self.buffer_lock:
                # 仅在非主动请求时填充日志缓冲区
                if not self.expect_response:
                    self.log_buffer.extend(data)
                self.data_buffer.extend(data)
                # logger.debug('当前缓冲区数据：[%s]', utils.byte_array_to_hex_string(self.data_buffer))
            
        # 尝试解析缓冲区中的数据，接收完整数据的超时时间设为1s
        if self.expect_response and len(self.data_buffer) >= MIN_DATA_LENGTH:
            # logger.debug('开始尝试解析数据')
            serial_message, message_status = SerialMessage.from_serial_data(self.data_buffer)
            # logger.debug('解析结果serial_message：%s', serial_message)
            # logger.debug('解析结果message_status：%s', message_status)
            if serial_message:
                # 解析成功，移除已解析的数据
                parsed_length = serial_message.data_length
                with self.buffer_lock:
                    
                    self.receive_buffer.append({
                        'data': self.data_buffer[:parsed_length],
                        'timestamp': self.last_receive_time  # 时间戳
                    })
                    # self.receive_buffer = self.data_buffer[:parsed_length]
                    self.data_buffer = self.data_buffer[parsed_length:]
                logger.debug('解析结果serial_message：%s', serial_message)
                return serial_message  # 返回解析后的数据用于后续处理
            else:
                # 解析失败，判断是否为数据格式错误
                if message_status in [SerialMessage.HEADER_ERROR, SerialMessage.CRC_ERROR, SerialMessage.END_SYMBOL_ERROR]:  # 数据格式错误
                    # 尝试找到下一个消息头
                    for i in range(1, len(self.data_buffer), 1):
                        if self.data_buffer[i:i + len(ValidValues.HEADER_LUX)] == ValidValues.HEADER_LUX:
                            # 找到下一个消息头，移除之前的无效数据
                            discarded_data = self.data_buffer[:i]
                            if discarded_data:
                                # logger.warning('丢弃无效数据: [%s]', utils.byte_array_to_hex_string(discarded_data))
                                logger.warning('丢弃无效数据%d字节', len(discarded_data))
                        
                            self.data_buffer = self.data_buffer[i:]
                            break
                    else:
                        # 没有找到下一个消息头，清空缓冲区
                        # logger.warning('丢弃无效数据: [%s]', utils.byte_array_to_hex_string(self.data_buffer))
                        logger.warning('丢弃无效数据%d字节', len(self.data_buffer))
                        self.data_buffer = bytearray()
                else:  
                    logger.debug('尝试解析数据失败，返回%s，准备接收下一个数据', message_status)
                    header_start_time = time.time()
                logger.debug('当前缓冲区数据：[%s]', utils.byte_array_to_hex_string(self.data_buffer))
                    
        else:
            # 非请求模式直接处理为日志数据
            if data:
                with self.buffer_lock:
                    self.log_buffer.extend(data)
                    self.data_buffer.clear()
        return None

    def generate_mock_data(self):
        '''
        生成模拟数据
        '''
        try:
            keys = ['vol', 'cur', 'pow']
            # 随机选择 1 到 3 个指标
            selected_keys = random.sample(keys, random.randint(1, 3))
            data_parts = []
            for key in selected_keys:
                # 生成随机值
                value = round(random.uniform(4, 15), 2)
                data_parts.append(f'{key}={value}')

            mock_data = ' '.join(data_parts).encode()
            # 使用 SerialMessage 生成要发送的数据
            data_type = b'\x01'  # 假设数据类型为 0x01
            command = b'\x02'    # 假设命令为 0x02
            serial_data = SerialMessage.generate_new_message(data_type, command, mock_data)
            return serial_data
        except Exception as e:
            logger.error('生成模拟数据时出错: %s', e)
            return None

    def get_sent_commands(self):
        """获取并清空已发送指令缓冲区"""
        with self.sent_lock:
            commands = self.sent_buffer.copy()
            self.sent_buffer.clear()
        return commands
    
    def get_received_data(self):
        """获取并清空接收数据缓冲区"""
        with self.buffer_lock:
            # received_data = bytes(self.receive_buffer)
            received_data = self.receive_buffer.copy()
            self.receive_buffer.clear()
        return received_data
    
    def send_request_with_retry(self, serial_message:SerialMessage):
        '''
        发送请求并处理重试逻辑

        :param request_data: 要发送的 SerialMessage 类型的请求数据
        :return:SerialMessage 若收到应答返回应答数据，若连续 3 次无应答返回 None
        '''
        self.expect_response = True  # 设置响应期待标志
        self.active_request_command = serial_message.command
        try:
            timeout = 1
            max_retries = 3
            # 使用 SerialMessage 生成要发送的数据
            if serial_message is not None:
                for retry_count in range(max_retries):
                    with self.buffer_lock:
                        self.data_buffer.clear()  # 发送前清空数据缓冲区
                    logger.info('开始第 %d 次请求，准备发送数据：%s', retry_count + 1, serial_message.full_data)
                    self.serial.send_data(serial_message.full_data)
                    start_time = time.time()
                    # 记录发送信息到缓冲区
                    with self.sent_lock:
                        self.sent_buffer.append({
                            'data': serial_message.full_data,
                            'retry': retry_count+1,
                            'timestamp': start_time  # 时间戳
                        })
                    while (time.time() - start_time) < timeout:
                        response_data = self.receive_data()
                        logger.debug('第 %d 次请求收到应答数据：%s', retry_count + 1, response_data)
                        if response_data is not None:
                            if response_data.data_type == ValidValues.DATA_TYPE_RESPONSE \
                                and response_data.command == serial_message.command:
                                
                                return response_data
                            else:
                                logger.warning('收到无效的应答数据，准备重试')
                        time.sleep(0.1)
                    logger.warning('第 %d 次请求无应答', retry_count + 1)
                logger.error('连续 %d 次请求无应答，放弃请求', max_retries)
            return None
        finally:
            self.expect_response = False  # 重置响应期待标志
            self.active_request_command = None
    
    def get_software_version(self):
        '''
        获取软件版本号
        '''
        logger.info('开始获取软件版本号')
        get_sw_ver_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_READ_SW_VERSION, ValidValues.DATA_EMPTY)
        response_message = self.send_request_with_retry(get_sw_ver_message)
        if response_message is not None:
            software_version = response_message.data
            return utils.array_to_ascii(software_version)
        logger.error('获取软件版本号失败')
        return None
    
    def reset_device(self):
        '''
        复位设备
        '''
        logger.info('开始复位设备')
        reset_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_RESET, ValidValues.DATA_EMPTY)
        response_message = self.send_request_with_retry(reset_message)
        if response_message is not None:
            if response_message.data == ValidValues.RESET_SUCCESS_DATA:
                logger.info('设备复位成功')
                return True
            else:
                logger.error('复位失败')
                return False
        logger.error('复位失败')
        return False
    
    def config_device(self, toml_path):
        '''
        配置设备
        :param toml_path: toml文件路径
        :return: 配置结果True/False message: 错误信息
        '''
        # 读取toml文件
        config, result = ConfigParams.from_toml_data(toml_path)
        if result == ConfigParams.NO_ERROR:
            # 发送配置数据
            logger.info('开始配置设备')
            config_message = SerialMessage.generate_new_message(
                ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_CONFIG_PARAMS, config.data)
            response_message = self.send_request_with_retry(config_message)
            message = 'SET_CONFIG_ERROR'
            if response_message is not None:
                if response_message.data == ValidValues.CONFIG_SUCCESS_DATA:
                    logger.info('设备配置成功')
                    # TODO 配置成功读取配置
                    read_data, read_date_str = self.read_device_config(True)
                    if read_data == config.data:
                        logger.info('读取配置一致')
                    else:
                        logger.error('读取配置不一致')
                        return False, f'{ConfigParams.CONFIG_CONSISTENCY_ERROR} : \n配置信息：\n{ConfigParams.to_config_str(config.data)}\n读取的配置信息：\n{read_date_str}'
                    return True, result
                
                else:
                    logger.error('配置失败')
                    return False, message
            logger.error('配置失败')
            return False, message
        else:
            logger.error('配置文件错误')
            return False, result
        
    def read_device_config(self, for_config=False):
        '''
        读取设备配置
        '''
        # 发送读取配置数据
        logger.info('开始读取设备配置')
        read_config_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_READ_PARAMS, ValidValues.DATA_EMPTY)
        response_message = self.send_request_with_retry(read_config_message)
        if response_message is not None:
            # 解析配置数据
            config_params, parse_result = ConfigParams.to_config_str(response_message.data)
            if config_params:
                logger.info('读取配置成功：\n%s', config_params)
                if for_config:
                    return response_message.data, config_params
                else:
                    return config_params, None
            else:
                logger.error('解析配置数据失败')
                return None, parse_result
        else:
            logger.error('读取配置失败')
            return None, None
        
    def get_key_status(self):
        '''
        获取密钥状态
        '''
        # 发送读取密钥状态数据
        logger.info('开始获取密钥状态')
        read_key_status_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_GET_KEY_STATUS, ValidValues.DATA_EMPTY)
        response_message = self.send_request_with_retry(read_key_status_message)
        if response_message is not None:
            # 解析密钥状态数据
            key_status, parse_result = response_message.to_key_status()
            if key_status:
                logger.info('获取密钥状态成功：%s', key_status)
                return key_status, None
            else:
                logger.error('解析密钥状态数据失败')
                return None, parse_result
        else:
            logger.error('获取密钥状态失败')
            return None, None

if __name__ == "__main__":
    # 创建 SerialModel 实例
    model = SerialModel()

    # 生成模拟数据
    mock_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_READ_SW_VERSION, ValidValues.DATA_EMPTY)
    if mock_message is not None:
        # 调用 send_request_with_retry 方法
        response = model.send_request_with_retry(mock_message)
        if response is not None:
            print("收到有效响应:", response)
        else:
            print("未收到有效响应")
    else:
        print("生成模拟数据失败")
