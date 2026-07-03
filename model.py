'''
Model类
处理数据

'''
import time
import random
import logging
import serial
import threading
from typing import Optional
from PySide6.QtCore import QObject, Signal

from utils.serial_handle import SerialOperator
from utils.data_processor import SerialMessage, ValidValues, ConfigParams, MIN_DATA_LENGTH
import utils.common_data_utils as utils
from utils.common_data_utils import pack_uint16_le, pack_uint32_le, unpack_uint16_le
from utils.flash_driver import (
    read_flash_driver_file,
    calculate_flash_driver_crc32,
    get_flash_driver_chunk,
)

logger = logging.getLogger(__name__)

class SerialModel(QObject):
    data_discarded_signal = Signal(dict)  # 类属性，所有实例共享

    def __init__(self):
        super().__init__()
        
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
        :return: (SerialMessage or None, discard_info or None)
                 discard_info = {'data': bytes, 'timestamp': float, 'reason': str}
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
           
        discard_info = None  # 丢弃信息，默认为 None
        
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
                                discard_info = {
                                    'data': bytes(discarded_data),
                                    'timestamp': self.last_receive_time,
                                    'reason': f'校验失败[{message_status}]'
                                }
                                logger.warning('丢弃无效数据%d字节', len(discarded_data))
                        
                            self.data_buffer = self.data_buffer[i:]
                            break
                    else:
                        # 没有找到下一个消息头，清空缓冲区
                        discarded_data = self.data_buffer
                        if discarded_data:
                            discard_info = {
                                'data': bytes(discarded_data),
                                'timestamp': self.last_receive_time,
                                'reason': f'校验失败[{message_status}]'
                            }
                            logger.warning('丢弃无效数据%d字节', len(discarded_data))
                        self.data_buffer = bytearray()
                else:  
                    logger.debug('尝试解析数据失败，返回%s，准备接收下一个数据', message_status)
                    header_start_time = time.time()
                logger.debug('当前缓冲区数据：[%s]', utils.byte_array_to_hex_string(self.data_buffer))
                    
        else:
            # expect_response=True 且数据不足以解析时，临时写入 log_buffer
            # （expect_response=False 时 log_buffer 已在上面写过，不要重复写）
            pass
        if discard_info:
            self.data_discarded_signal.emit(discard_info)
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
    
    def send_request_with_retry(self, serial_message:SerialMessage, timeout=1) -> Optional[SerialMessage]:
        '''
        发送请求并处理重试逻辑

        重试触发条件（满足任一则重发下一轮 for 循环，最多 3 轮）：
            1. 通讯超时（1 秒内无任何响应）
            2. 收到响应但 data_type 不是 RESPONSE
            3. 收到响应但 command 与请求不匹配

        注意：否定响应（status_code 非 0）不属于重试条件，视为有效响应立即返回，
              由调用方自行检查 status_code 决定后续处理。

        :param serial_message: 要发送的 SerialMessage 类型的请求数据
        :return: 收到有效响应（肯定/否定均可）返回 SerialMessage，连续 3 次均未收到返回 None
        '''
        self.expect_response = True  # 设置响应期待标志
        self.active_request_command = serial_message.command
        try:
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

    def get_uid(self):
        '''
        读取UID
        TODO 未返回读取失败原因
        :return: UID字符串(16字节HEX) 或 None
        '''
        logger.info('开始读取UID')
        get_uid_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_READ_UID, ValidValues.DATA_EMPTY)
        response_message = self.send_request_with_retry(get_uid_message)
        
        if response_message is None:
            logger.error('读取UID失败：无响应')
            return None
        
        uid_str = utils.byte_array_to_hex_string(response_message.data)
        return uid_str

    def send_flash_driver_start(self):
        '''
        通知传输FlashDriver（OTA命令，通知工具开始下载，实际传输由CAN完成）
        TODO
        :return: True成功，False失败
        '''
        logger.info('开始通知传输FlashDriver')
        message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_SEND_FLASH_DRIVER, ValidValues.DATA_EMPTY)
        response = self.send_request_with_retry(message, timeout=30)  # OTA命令需要更长时间
        if response is None:
            error_msg = '通知下载FlashDriver超时未响应'
            logger.error(error_msg)
            return False, error_msg
        if len(response.data) >= 2 and response.data[:2] == ValidValues.RESET_SUCCESS_DATA:
            logger.info('下载FlashDriver成功')
            return True, ""
        else:
            logger.error('通知传输FlashDriver失败：状态码错误 %s', response.data[:2].hex() if len(response.data) >= 2 else 'N/A')
            return False, f'收到负响应{response.data[:2].hex()}'

    def write_qi_key(self, key_hex: str):
        '''
        写入Qi密钥
        TODO
        :param key_hex: 32字节HEX字符串
        :return: True成功，False失败
        '''
        logger.info('开始写入Qi密钥')
        key_data = utils.hex_str_to_byte_array(key_hex)
        message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_WRITE_QI_KEY, key_data)
        response = self.send_request_with_retry(message)
        if response is None:
            logger.error('写入Qi密钥失败：无响应')
            return False
        if len(response.data) >= 2 and response.data[:2] == ValidValues.RESET_SUCCESS_DATA:
            logger.info('写入Qi密钥成功')
            return True
        else:
            logger.error('写入Qi密钥失败：状态码错误 %s', response.data[:2].hex() if len(response.data) >= 2 else 'N/A')
            return False

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

    def input_flash_driver(self, file_path):
        '''
        导入 FlashDriver 到黑盒子
        :param file_path: FlashDriver bin 文件路径
        :return: (True, None) 成功，(False, error_message) 失败
        '''
        # 读取 FlashDriver 文件
        logger.info('开始下载 FlashDriver: %s', file_path)
        flash_driver_data = read_flash_driver_file(file_path)
        if flash_driver_data is None:
            logger.error('读取 FlashDriver 文件失败')
            return False, '读取 FlashDriver 文件失败'
        
        # 计算文件总长度
        total_length = len(flash_driver_data)
        logger.info('FlashDriver 文件大小: %d 字节', total_length)
        
        if total_length == 0:
            logger.error('FlashDriver 文件为空')
            return False, 'FlashDriver 文件为空'
        
        # 计算 CRC32 (小端序)
        crc32_value = calculate_flash_driver_crc32(flash_driver_data)
        
        # 步骤1: 发送启动传输命令 (0x0201)
        logger.info('发送启动传输命令')
        start_data = pack_uint16_le(total_length)
        start_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_FLASH_START, start_data)
        response_message = self.send_request_with_retry(start_message)
        
        if response_message is None:
            logger.error('启动传输命令无应答')
            return False, '启动传输命令无应答'
        
        status_code = response_message.data[0] if response_message.data else 0xFF
        if status_code != 0x00:
            status_messages = {
                0x01: '设备忙',
                0x02: '空间不足'
            }
            error_msg = status_messages.get(status_code, f'未知错误 0x{status_code:02X}')
            logger.error('启动传输失败: %s', error_msg)
            return False, error_msg
        
        logger.info('启动传输成功，准备开始发送数据')

        # 步骤2: 分包发送数据 (0x0202)
        chunk_size = ValidValues.MAX_APP_DATA_LENGTH
        offset = 0
        max_retry = 3

        while offset < total_length:
            chunk_result = get_flash_driver_chunk(flash_driver_data, chunk_size, offset)
            if chunk_result is None:
                logger.error('分片越界: offset=%d', offset)
                return False, f'分片越界: offset={offset}'

            _, data_chunk = chunk_result

            packet_data = pack_uint16_le(offset) + data_chunk
            packet_message = SerialMessage.generate_new_message(
                ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_FLASH_DATA, packet_data)

            logger.debug('发送数据包: 偏移=0x%04X, 长度=%d', offset, len(data_chunk))

            response_message = self.send_request_with_retry(packet_message)
            if response_message is None:
                logger.error('数据包无应答: 偏移=0x%04X', offset)
                return False, f'数据包无应答: 偏移=0x{offset:04X}'

            resp_data = response_message.data
            if len(resp_data) < 3:
                logger.error('数据包应答格式错误')
                return False, '数据包应答格式错误'

            resp_status = resp_data[0]
            expected_offset = unpack_uint16_le(resp_data[1:3])

            if resp_status != 0x00:
                logger.error('数据包写入失败，状态码=0x%02X，期望偏移=0x%04X', resp_status, expected_offset)
                return False, f'写入失败，期望偏移=0x{expected_offset:04X}'

            # 处理重传：设备期望的偏移量不大于当前偏移，说明要求重传
            if expected_offset <= offset:
                retry_count = 0
                while retry_count < max_retry and expected_offset <= offset:
                    logger.warning('设备要求重传: 期望偏移=0x%04X, 当前偏移=0x%04X (重试 %d/%d)',
                                   expected_offset, offset, retry_count + 1, max_retry)

                    chunk_result = get_flash_driver_chunk(flash_driver_data, chunk_size, expected_offset)
                    if chunk_result is None:
                        logger.error('重传分片越界: offset=%d', expected_offset)
                        return False, f'重传分片越界: offset={expected_offset}'

                    _, data_chunk = chunk_result

                    packet_data = pack_uint16_le(expected_offset) + data_chunk
                    packet_message = SerialMessage.generate_new_message(
                        ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_FLASH_DATA, packet_data)

                    response_message = self.send_request_with_retry(packet_message)
                    if response_message is None:
                        logger.error('重传无应答: 偏移=0x%04X', expected_offset)
                        return False, f'重传无应答: 偏移=0x{expected_offset:04X}'

                    resp_data = response_message.data
                    if len(resp_data) < 3:
                        logger.error('重传应答格式错误')
                        return False, '重传应答格式错误'

                    resp_status = resp_data[0]
                    expected_offset = unpack_uint16_le(resp_data[1:3])

                    if resp_status != 0x00:
                        logger.error('重传写入失败，状态码=0x%02X，期望偏移=0x%04X', resp_status, expected_offset)
                        return False, f'重传写入失败，期望偏移=0x{expected_offset:04X}'

                    retry_count += 1

                if retry_count >= max_retry:
                    logger.error('重传 %d 次仍未成功，放弃 offset=0x%04X', max_retry, offset)
                    return False, f'重传 {max_retry} 次仍未成功，放弃 offset=0x{offset:04X}'

                offset = expected_offset
                logger.debug('重传成功，偏移量更新为: 0x%04X', offset)
            else:
                offset = expected_offset
                logger.debug('数据包发送成功，偏移量更新为: 0x%04X', offset)
        
        # 步骤3: 发送结束与总校验命令 (0x0203)
        logger.info('发送结束与总校验命令')
        end_data = pack_uint32_le(crc32_value)
        end_message = SerialMessage.generate_new_message(
            ValidValues.DATA_TYPE_REQUEST, ValidValues.COMMANDS_FLASH_END, end_data)
        response_message = self.send_request_with_retry(end_message)
        
        if response_message is None:
            logger.error('结束与总校验命令无应答')
            return False, '结束与总校验命令无应答'
        
        verify_result = response_message.data[0] if response_message.data else 0xFF
        if verify_result != 0x00:
            verify_messages = {
                0x01: 'CRC32校验失败',
                0x02: '总长度不匹配'
            }
            error_msg = verify_messages.get(verify_result, f'未知错误 0x{verify_result:02X}')
            logger.error('总校验失败: %s', error_msg)
            return False, error_msg
        
        logger.info('FlashDriver 下载成功')
        return True, None

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
