'''
    业务相关的数据处理
'''
import common_data_utils as utils
import file_utils as file_utils

from logger import logger

# 定义消息各部分的长度（占字节数）
HEADER_LENGTH       = 3     # 数据头长度
DATA_TYPE_LENGTH    = 1     # 数据类型长度
COMMAND_LENGTH      = 2     # 命令长度
DATA_LENGTH_BYTES   = 2     # 数据体长度
CRC_LENGTH          = 1     # CRC 校验码长度
END_SYMBOL_LENGTH   = 2     # 结束符长度
MIN_DATA_LENGTH     = HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES + CRC_LENGTH + END_SYMBOL_LENGTH   # 数据体最小长度
MAX_APP_DATA_LENGTH = 128   # APP业务数据体最大长度
MAX_OTA_DATA_LENGTH = 4096  # OTA业务数据体最大长度
KEY_STATUS_MIN_LENGTH = 5   # 密钥状态最小长度,通用did 4209内容长度10个字节, Byte0-4,5字节显示5个密钥状态

class ValidValues:
    '''
    定义有效的消息头、数据类型、命令和结束符
    '''
    # 定义消息头、数据类型、命令和结束符
    HEADER_LUX = b'\x4C\x75\x78'     # 数据头固定为：“Lux”
    DATA_TYPE_REQUEST   = b'\x00'     # 数据类型 00：表示请求
    DATA_TYPE_RESPONSE  = b'\x01'     # 数据类型 01：表示应答
    COMMANDS_READ_SW_VERSION    = b'\x00\x01'     # 命令 00 01：读软件版本号
    COMMANDS_CONFIG_PARAMS      = b'\x00\x02'     # 命令 00 02：参数配置
    COMMANDS_READ_PARAMS        = b'\x00\x03'     # 命令 00 03：参数读取
    COMMANDS_GET_KEY_STATUS     = b'\x00\x04'     # 命令 00 04：获取密钥状态
    COMMANDS_RESET              = b'\x01\x01'     # 命令 01 01：复位
    DATA_EMPTY = b''     # 数据体为空
    END_SYMBOL = b'\x0D\x0A'     # 结束符为：\r\n，转16进制为：0x0D 0x0A

    RESET_SUCCESS_DATA = b'\x00\x00'     # 复位成功数据
    CONFIG_SUCCESS_DATA = b'\x00\x00'     # 参数配置成功数据
    FAIL_DATA     = b'\xFF\xFF'     # 失败数据

    # 定义消息头、数据类型、命令和结束符的集合
    HEADERS = [HEADER_LUX]     # 数据头固定为：“Lux”
    DATA_TYPES = [DATA_TYPE_REQUEST, DATA_TYPE_RESPONSE] # 数据类型 00：表示请求，01：表示应答
    COMMANDS = [COMMANDS_READ_SW_VERSION, COMMANDS_CONFIG_PARAMS, COMMANDS_READ_PARAMS, COMMANDS_GET_KEY_STATUS, COMMANDS_RESET]   # 命令 00 01：读软件版本号，00 02：参数配置，00 03：参数读取，00 04：获取密钥状态，01 01：复位
    END_SYMBOLS = [END_SYMBOL]     # 结束符为：\r\n，转16进制为：0x0D 0x0A


    # 定义 CAN 配置常量
    CAN_CONFIG_SECTION = 'CAN_config'
    CAN_TYPE_KEY = 'type'
    BAUDRATE_KEY = 'baudrate'
    REQUEST_ID_KEY = 'request_id'
    RESPONSE_ID_KEY = 'response_id'

    # 定义诊断 DID 配置常量
    DIAG_DID_SECTION = 'diag_did'
    GET_KEY_STATUS_KEY = 'get_key_status'
    READ_WRITE_KEY_KEY = 'read_write_key'

    # 定义网络管理配置常量
    NM_CONFIG_SECTION = 'nm_config'
    NM_ENABLED_KEY = 'nm_enabled'
    NM_ID_KEY = 'nm_id'
    NM_PERIOD_KEY = 'nm_period'
    
    # 定义通信类型到数值的映射
    CAN_TYPE_MAPPING = {
        'CAN': b'\x01',
        'CANFD': b'\x02',
        'LIN': b'\x03',
        'UART': b'\x04'
    }  

    CAN_TYPE_MAPPING_REVERSE = {
        b'\x01': 'CAN',
        b'\x02': 'CANFD',
        b'\x03': 'LIN',
        b'\x04': 'Uart'
    }  

class SerialMessage:
    '''
    串口消息类，用于封装串口消息的各个字段。
    '''
    HEADER_ERROR = 'HEADER_ERROR'
    DATA_TYPE_ERROR = 'DATA_TYPE_ERROR'
    COMMAND_ERROR = 'COMMAND_ERROR'
    CRC_ERROR = 'CRC_ERROR'
    END_SYMBOL_ERROR = 'END_SYMBOL_ERROR'
    DATA_LENGTH_ERROR = 'DATA_LENGTH_ERROR'
    DATA_LENGTH_EXCEED_ERROR = 'DATA_LENGTH_EXCEED_ERROR'   # 数据体长度超过最大长度
    DATA_LENGTH_SHORT_ERROR = 'DATA_LENGTH_SHORT_ERROR'   # 数据体长度不足最小长度
    DATA_LENGTH_MISMATCH_ERROR = 'DATA_LENGTH_MISMATCH_ERROR'   # 数据体长度与实际长度不匹配
    NO_ERROR = 'NO_ERROR'

    DATA_RESPONSE_NONE = 'DATA_RESPONSE_NONE'
    DATA_RESPONSE_0000 = 'DATA_RESPONSE_0000'
    DATA_RESPONSE_FFFF = 'DATA_RESPONSE_FFFF'

    def __init__(self, serial_data, data_length, data_type, command, data):
        self.full_data = serial_data
        self.data_length = data_length
        self.data_type = data_type
        self.command = command
        self.data = data

    @classmethod
    def from_serial_data(cls, serial_data):
        '''
        从串口接收到的原始数据中解析出消息的各个字段。

        :param serial_data: 从串口接收到的原始数据
        '''
        # TODO 调用该方法代表接收到了一条完整的消息,清空上一次的数据？不同的实体？

        # 输出原始数据，按照XX XX XX格式
        logger.debug('Attempt to parse serial data: [%s]', utils.byte_array_to_hex_string(serial_data))
        # 计算所需的最小数据长度
        # min_length = HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES + CRC_LENGTH + END_SYMBOL_LENGTH
        if len(serial_data) < MIN_DATA_LENGTH:
            logger.error('Received data length is insufficient. Expected at least %d bytes, got %d bytes.', MIN_DATA_LENGTH, len(serial_data))
            return None, cls.DATA_LENGTH_SHORT_ERROR
        
        # 解析消息字段
        header = serial_data[:HEADER_LENGTH]
        data_type = serial_data[HEADER_LENGTH:HEADER_LENGTH + DATA_TYPE_LENGTH]
        command = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH:HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH]
        data_body_length_bytes = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH:HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES]
        data_body_length = int.from_bytes(data_body_length_bytes, byteorder='little', signed=False)

        # 检查数据体部分长度是否足够
        expected_total_length = MIN_DATA_LENGTH + data_body_length
        if len(serial_data) < expected_total_length:
            logger.error('Received data length is insufficient for data body. Expected %d bytes, got %d bytes.', expected_total_length, len(serial_data))
            return None, cls.DATA_LENGTH_SHORT_ERROR
        
        data_length = expected_total_length
        data = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES:HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES + data_body_length]
        data_crc = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES + data_body_length:HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES + data_body_length + CRC_LENGTH]
        
        # 结束符
        end_symbol = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES + data_body_length + CRC_LENGTH:data_length]
        if len(end_symbol) > END_SYMBOL_LENGTH:
            logger.warning('Received more than %d bytes for end_symbol. Truncating to %d bytes.', END_SYMBOL_LENGTH, END_SYMBOL_LENGTH)
            end_symbol = end_symbol[:END_SYMBOL_LENGTH]

        # 消息头格式判定
        if header not in ValidValues.HEADERS:
            logger.error('Invalid message header: %s', header)
            return None, cls.HEADER_ERROR
        # 数据类型判定
        if data_type not in ValidValues.DATA_TYPES:
            logger.error('Invalid message data type: %s', data_type)
            return None, cls.DATA_TYPE_ERROR
        # 命令判定
        if command not in ValidValues.COMMANDS:
            logger.error('Unknown message command: %s', command)
            return None, cls.COMMAND_ERROR
        # CRC校验
        expected_crc = utils.calculate_crc_bytes(data)
        if data_crc != expected_crc:
            logger.error('CRC check failed. Expected: %s, Got: %s', expected_crc, data_crc)
            return None, cls.CRC_ERROR
        # 结束符号判定
        if end_symbol not in ValidValues.END_SYMBOLS:
            logger.error('Invalid message end symbol: %s', end_symbol)
            return None, cls.END_SYMBOL_ERROR
        
        return cls(serial_data, data_length, data_type, command, data), cls.NO_ERROR
    
    @staticmethod
    def get_data_length(serial_data):
        '''
        获取数据体长度。

        :param data: 数据体
        :return: 数据体长度
        '''
        if len(serial_data) >= HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES:
            header = serial_data[:HEADER_LENGTH]
            # 消息头格式判定
            if header not in ValidValues.HEADERS:
                logger.error('Invalid message header: %s', header)
                return 0
            
            data_type = serial_data[HEADER_LENGTH:HEADER_LENGTH + DATA_TYPE_LENGTH]
            # 数据类型判定
            if data_type not in ValidValues.DATA_TYPES:
                logger.error('Invalid message data type: %s', data_type)
                return 0
            
            command = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH:HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH]
            # 命令判定
            if command not in ValidValues.COMMANDS:
                logger.error('Unknown message command: %s', command)
                return 0
            
            # 数据体长度
            data_body_length_bytes = serial_data[HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH:HEADER_LENGTH + DATA_TYPE_LENGTH + COMMAND_LENGTH + DATA_LENGTH_BYTES]
            data_body_length = int.from_bytes(data_body_length_bytes, byteorder='little', signed=False)

            return data_body_length
        return 0
        
    def to_key_status(self):
        '''
        将数据体转换为密钥状态。

        :param data: 数据体
        :return: 密钥状态， 错误信息
        '''
        if self.data is None:
            logger.error('Data is None')
            return None, self.DATA_RESPONSE_NONE
        
        if self.data == ValidValues.FAIL_DATA:
            logger.error('Data is FAIL_DATA， 读取密钥状态，返回参数不满足 %s', utils.little_endian_array_to_hex_str(self.data))
            return None, self.DATA_RESPONSE_FFFF
        
        if len(self.data) < KEY_STATUS_MIN_LENGTH:
            logger.error('Data length is less than %d, data: %s', KEY_STATUS_MIN_LENGTH, utils.little_endian_array_to_hex_str(self.data))
            return None, self.DATA_LENGTH_SHORT_ERROR
        
        key_status = []
        for i in range(0, KEY_STATUS_MIN_LENGTH):  # 只处理前 5 个字节
            byte = self.data[i]
            download_status = (byte & 0x01) == 0x01  # 提取 bit0
            enable_status = (byte & 0x10) == 0x10    # 提取 bit4
            key_status.append((download_status, enable_status))

        return key_status, self.NO_ERROR
        


            

    @staticmethod
    def _generate_serial_bytes(data_type, command, data):
        '''
        生成符合格式要求的字节数据，供内部方法调用。

        :param data_type: 消息的数据类型 length:1
        :param command: 消息的命令 length:2
        :param data: 消息的数据体
        :return: 符合格式要求的字节数据或 None（如果参数无效）
        '''
        if data_type not in ValidValues.DATA_TYPES:
            logger.error('Invalid data type: %s', data_type)
            return None
        if command not in ValidValues.COMMANDS:
            logger.error('Invalid command: %s', command)
            return None

        header = ValidValues.HEADERS[0]
        data_length = len(data).to_bytes(DATA_LENGTH_BYTES, byteorder='little', signed=False)
        data_crc = utils.calculate_crc_bytes(data)
        end_symbol = ValidValues.END_SYMBOLS[0]

        serial_data = header + data_type + command + data_length + data + data_crc + end_symbol
        logger.debug('Generate serial data: [%s]', utils.byte_array_to_hex_string(serial_data))
        
        return serial_data

    @classmethod
    def generate_new_message(cls, data_type, command, data):
        '''
        根据指定的消息字段生成符合格式要求的字节数据，并创建新的 SerialMessage 实例。

        :param data_type: 消息的数据类型
        :param command: 消息的命令
        :param data: 消息的数据体
        :return: 新的 SerialMessage 实例或 None（如果参数无效）
        '''
        serial_data = cls._generate_serial_bytes(data_type, command, data)
        if serial_data is None:
            return None
        return cls(serial_data, len(serial_data), data_type, command, data)

    def generate_serial_data(self, data_type=None, command=None, data=None):
        '''
        根据指定的消息字段生成符合格式要求的字节数据，并更新当前实例的属性。

        :param data_type: 消息的数据类型，默认为实例当前的数据类型
        :param command: 消息的命令，默认为实例当前的命令
        :param data: 消息的数据体，默认为实例当前的数据体
        '''
        if data_type is None:
            data_type = self.data_type
        if command is None:
            command = self.command
        if data is None:
            data = self.data

        serial_data = self._generate_serial_bytes(data_type, command, data)
        if serial_data is None:
            return None
        self.full_data = serial_data
        self.data_type = data_type
        self.command = command
        self.data = data

    def __str__(self):
        data_type_str = '请求' if self.data_type == b'\x00' else '应答'
        match self.command:
            case ValidValues.COMMANDS_READ_SW_VERSION:
                command_str = '读取软件版本号'
            case ValidValues.COMMANDS_CONFIG_PARAMS:
                command_str = '参数配置'
            case ValidValues.COMMANDS_READ_PARAMS:
                command_str = '参数读取'
            case ValidValues.COMMANDS_GET_KEY_STATUS:
                command_str = '获取密钥状态'
            case ValidValues.COMMANDS_RESET:
                command_str = '复位'
            case _:
                command_str = '未知命令'
        if self.full_data is None:
            self.generate_serial_data()
        return f'原始数据：{self.full_data}\r\n原始数据长度：{self.data_length}bytes，数据类型：0x{self.data_type.hex()} {data_type_str}，命令：0x{self.command.hex()} {command_str}，数据：{utils.byte_array_to_hex_string(self.data)}（ASCII：{utils.array_to_ascii(self.data)}）)'

class ConfigParams:
    '''
    配置参数类，用于封装配置参数的各个字段。
    '''
    NO_ERROR = 'NO_ERROR'
    PATH_ERROR = 'PATH_ERROR'
    CONFIG_PARAMS_ERROR = 'CONFIG_PARAMS_ERROR'
    CAN_TYPE_ERROR = 'CAN_TYPE_ERROR'
    BAUDRATE_ERROR = 'BAUDRATE_ERROR'
    REQUEST_ID_ERROR = 'REQUEST_ID_ERROR'
    RESPONSE_ID_ERROR = 'RESPONSE_ID_ERROR'
    GET_KEY_STATUS_ERROR = 'GET_KEY_STATUS_ERROR'
    READ_WRITE_KEY_ERROR = 'READ_WRITE_KEY_ERROR'
    NM_ID_ERROR = 'NM_ID_ERROR'
    NM_PERIOD_ERROR = 'NM_PERIOD_ERROR'
    NM_ENABLED_ERROR = 'NM_ENABLED_ERROR'

    CONFIG_CONSISTENCY_ERROR = 'CONFIG_CONSISTENCY_ERROR'
    LENGTH_TOO_SHORT_ERROR = 'LENGTH_TOO_SHORT_ERROR'
    LENGTH_TOO_LONG_ERROR = 'LENGTH_TOO_LONG_ERROR'
    PARSE_ERROR = 'PARSE_ERROR'

    
    # 定义数据提取的起始位置常量和长度
    CAN_TYPE_START = 0
    CAN_TYPE_LENGTH = 1
    BAUDRATE_LENGTH = 3
    REQUEST_ID_LENGTH = 2
    RESPONSE_ID_LENGTH = 2
    GET_KEY_STATUS_LENGTH = 2
    READ_WRITE_KEY_LENGTH = 2
    NM_ENABLED_LENGTH = 1
    NM_ID_LENGTH = 2
    NM_PERIOD_LENGTH = 2

    BAUDRATE_START = CAN_TYPE_START + CAN_TYPE_LENGTH
    REQUEST_ID_START = BAUDRATE_START + BAUDRATE_LENGTH
    RESPONSE_ID_START = REQUEST_ID_START + REQUEST_ID_LENGTH
    GET_KEY_STATUS_START = RESPONSE_ID_START + RESPONSE_ID_LENGTH
    READ_WRITE_KEY_START = GET_KEY_STATUS_START + GET_KEY_STATUS_LENGTH
    NM_ENABLED_START = READ_WRITE_KEY_START + READ_WRITE_KEY_LENGTH
    NM_ID_START = NM_ENABLED_START + NM_ENABLED_LENGTH
    NM_PERIOD_START = NM_ID_START + NM_ID_LENGTH

    def __init__(self, data, toml_path):
        self.toml_path = toml_path
        self.data = data

    @classmethod
    def from_toml_data(cls, toml_path):
        '''
        从 TOML 数据中解析出配置参数的各个字段。

        :param toml_path: TOML 文件路径
        '''
        try:
            config = file_utils.read_toml_file(toml_path)
            if config is None or config == {}:
                return None, cls.PATH_ERROR

            can_config = config.get(ValidValues.CAN_CONFIG_SECTION, {})
            diag_did = config.get(ValidValues.DIAG_DID_SECTION, {})
            nm_config = config.get(ValidValues.NM_CONFIG_SECTION, {})

            # 定义一个辅助函数用于转换并捕获异常
            def convert_and_catch(param_name, value, length):
                try:
                    return utils.int_to_fixed_bytes(value, length)
                except OverflowError:
                    logger.error(f'参数 {param_name} ({value}) 无法用 {length} 字节表示。')
                    return None, cls.PARSE_ERROR

            can_type = cls.convert_can_type(can_config.get(ValidValues.CAN_TYPE_KEY))
            if can_type is None:
                logger.error('参数 can_type 转换失败。')
                return None, cls.CAN_TYPE_ERROR

            baudrate = convert_and_catch(ValidValues.BAUDRATE_KEY, can_config.get(ValidValues.BAUDRATE_KEY), cls.BAUDRATE_LENGTH)
            if baudrate is None:
                return None, cls.BAUDRATE_ERROR

            request_id = convert_and_catch(ValidValues.REQUEST_ID_KEY, can_config.get(ValidValues.REQUEST_ID_KEY), cls.REQUEST_ID_LENGTH)
            if request_id is None:
                return None, cls.REQUEST_ID_ERROR

            response_id = convert_and_catch(ValidValues.RESPONSE_ID_KEY, can_config.get(ValidValues.RESPONSE_ID_KEY), cls.RESPONSE_ID_LENGTH)
            if response_id is None:
                return None, cls.RESPONSE_ID_ERROR

            get_key_status = convert_and_catch(ValidValues.GET_KEY_STATUS_KEY, diag_did.get(ValidValues.GET_KEY_STATUS_KEY), cls.GET_KEY_STATUS_LENGTH)
            if get_key_status is None:
                return None, cls.GET_KEY_STATUS_ERROR

            read_write_key = convert_and_catch(ValidValues.READ_WRITE_KEY_KEY, diag_did.get(ValidValues.READ_WRITE_KEY_KEY), cls.READ_WRITE_KEY_LENGTH)
            if read_write_key is None:
                return None, cls.READ_WRITE_KEY_ERROR

            nm_enabled = cls.convert_nm_enabled(nm_config.get(ValidValues.NM_ENABLED_KEY))
            if nm_enabled is None:
                logger.error('参数 nm_enabled 转换失败。')
                return None, cls.NM_ENABLED_ERROR

            nm_id = convert_and_catch(ValidValues.NM_ID_KEY, nm_config.get(ValidValues.NM_ID_KEY), cls.NM_ID_LENGTH)
            if nm_id is None:
                return None, cls.NM_ID_ERROR

            nm_period = convert_and_catch(ValidValues.NM_PERIOD_KEY, nm_config.get(ValidValues.NM_PERIOD_KEY), cls.NM_PERIOD_LENGTH)
            if nm_period is None:
                return None, cls.NM_PERIOD_ERROR

            data = can_type + baudrate + request_id + response_id + get_key_status + read_write_key + nm_enabled + nm_id + nm_period
            return cls(data, toml_path), cls.NO_ERROR

        except Exception as e:
            logger.error('解析 TOML 文件时出现未知错误: %s', e)
            return None, cls.CONFIG_PARAMS_ERROR

    @staticmethod
    def convert_can_type(can_type:str):
        '''
        将 CAN 类型字符串转换为对应的字节数值。
        如果输入的类型不在映射中，则返回 None。
        :param can_type: 通信类型字符串，如 'CAN', 'CANFD', 'LIN', 'Uart'
        :return: 对应的字节数值，如 b'\x01', b'\x02', b'\x03', b'\x04'
        '''
        return ValidValues.CAN_TYPE_MAPPING.get(can_type.upper())
    
    @staticmethod
    def convert_baudrate(can_type:str, baudrate_str):
        '''
        根据通信类型将通信速率字符串转换为三位小端字节。

        :param can_type: 通信类型，如 'CAN', 'CANFD', 'LIN', 'Uart'
        :param baudrate_str: 通信速率字符串，如 '500K', '2M', '19200'
        :return: 三位小端字节
        '''
        # 处理 CAN 或 CANFD 类型
        if can_type.upper() in ['CAN', 'CANFD']:
            if baudrate_str.endswith('K'):
                baudrate = int(baudrate_str[:-1])
            elif baudrate_str.endswith('M'):
                baudrate = int(baudrate_str[:-1]) * 1000
            else:
                baudrate = int(baudrate_str)
        # 处理 LIN 或 UART 类型
        else:
            baudrate = int(baudrate_str)
        
        # 转换为三位小端字节
        return baudrate.to_bytes(3, byteorder='little')
    
    @staticmethod
    def convert_nm_enabled(nm_enabled):
        '''
        将 nm_enabled 转换为byte。

        :param nm_enabled: 要转换的值，True 或 False
        :return: 转换后的 byte 值
        '''
        if nm_enabled:
            return b'\x01'
        else:
            return b'\x00'

    @staticmethod
    def to_config_str(data):
        '''
        将 ConfigParams 实例中的数据转换为易读的配置字符串。

        :return: 包含配置数据的字符串
        '''
        # 计算所需的最小数据长度
        length = ConfigParams.NM_PERIOD_START + ConfigParams.NM_PERIOD_LENGTH
        if len(data) < length:
            logger.error(f'读取到的配置信息长度不足，需要 {length} 字节，实际只有 {len(data)} 字节，读取到 [{utils.byte_array_to_hex_string(data)}]。')
            return None, ConfigParams.LENGTH_TOO_SHORT_ERROR
        elif len(data) > length:
            logger.error(f'读取到的配置信息长度超过预期，需要 {length} 字节，实际有 {len(data)} 字节，读取到 [{utils.byte_array_to_hex_string(data)}]。')
            return None, ConfigParams.LENGTH_TOO_LONG_ERROR

        try:

            # 提取各部分数据
            can_type = ConfigParams._extract_can_type(data)
            baudrate = ConfigParams._extract_baudrate(data)
            request_id = ConfigParams._extract_request_id(data)
            response_id = ConfigParams._extract_response_id(data)
            get_key_status = ConfigParams._extract_get_key_status(data)
            read_write_key = ConfigParams._extract_read_write_key(data)
            nm_enabled = ConfigParams._extract_nm_enabled(data)
            nm_id = ConfigParams._extract_nm_id(data)
            nm_period = ConfigParams._extract_nm_period(data)

            # 转换波特率
            if can_type in ['CAN', 'CANFD']:  # CAN 或 CANFD
                if baudrate >= 1000:
                    baudrate_str = f'{baudrate // 1000}M'
                else:
                    baudrate_str = f'{baudrate}K'
            else:
                baudrate_str = str(baudrate)

            # 转换 ID 为十六进制
            request_id_str = hex(request_id)
            response_id_str = hex(response_id)
            get_key_status_str = hex(get_key_status)
            read_write_key_str = hex(read_write_key)
            nm_id_str = hex(nm_id)

            # 转换网络管理使能状态
            nm_enabled_str = '使能' if nm_enabled else '不使能'

            return f'通信类型：{can_type}\n' \
                f'通信速率：{baudrate_str}\n' \
                f'诊断请求 ID：{request_id_str}\n' \
                f'诊断响应 ID：{response_id_str}\n' \
                f'获取密钥状态 DID：{get_key_status_str}\n' \
                f'读写 DID：{read_write_key_str}\n' \
                f'网络管理报文使能：{nm_enabled_str}\n' \
                f'网络管理 ID：{nm_id_str}\n' \
                f'网络管理报文周期：{nm_period}MS', ConfigParams.NO_ERROR
        
        except Exception as e:
            # 记录异常信息
            logger.error(f'转换配置数据为字符串时出错: {e}')
            return None, ConfigParams.PARSE_ERROR
       
    # TODO 预留功能，写回toml文件
    @staticmethod 
    def to_toml_data(data, path):
        '''
        将 ConfigParams 实例中的数据转换回 TOML 格式的数据。

        :return: 包含配置数据的字典，可用于生成 TOML 文件
        '''
        # 提取各部分数据
        can_type = ConfigParams._extract_can_type(data)
        baudrate = ConfigParams._extract_baudrate(data)
        request_id = ConfigParams._extract_request_id(data)
        response_id = ConfigParams._extract_response_id(data)
        get_key_status = ConfigParams._extract_get_key_status(data)
        read_write_key = ConfigParams._extract_read_write_key(data)
        nm_enabled = ConfigParams._extract_nm_enabled(cdata)
        nm_id = ConfigParams._extract_nm_id(data)
        nm_period = ConfigParams._extract_nm_period(data)

        # 构建 TOML 数据字典
        toml_data = {
            ValidValues.CAN_CONFIG_SECTION: {
                ValidValues.CAN_TYPE_KEY: can_type,
                ValidValues.BAUDRATE_KEY: baudrate,
                ValidValues.REQUEST_ID_KEY: request_id,
                ValidValues.RESPONSE_ID_KEY: response_id
            },
            ValidValues.DIAG_DID_SECTION: {
                ValidValues.GET_KEY_STATUS_KEY: get_key_status,
                ValidValues.READ_WRITE_KEY_KEY: read_write_key
            },
            ValidValues.NM_CONFIG_SECTION: {
                ValidValues.NM_ENABLED_KEY: nm_enabled,
                ValidValues.NM_ID_KEY: nm_id,
                ValidValues.NM_PERIOD_KEY: nm_period
            }
        }

        return toml_data

    @staticmethod
    def _extract_can_type(data):
        '''
        提取 CAN 类型
        :param data: 配置数据
        :return: CAN 类型的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.CAN_TYPE_START + ConfigParams.CAN_TYPE_LENGTH:
            logger.error('数据长度不足，无法提取 CAN 类型')
            return None
        can_type_byte = data[ConfigParams.CAN_TYPE_START:ConfigParams.CAN_TYPE_START + ConfigParams.CAN_TYPE_LENGTH]
        # 将 bytearray 转换为 bytes 类型
        can_type_bytes = bytes(can_type_byte)
        return ValidValues.CAN_TYPE_MAPPING_REVERSE.get(can_type_bytes, f'未知类型{can_type_bytes.hex()}')

    @staticmethod
    def _extract_baudrate(data):
        '''
        提取波特率数据
        :param data: 配置数据
        :return: 波特率的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.BAUDRATE_START + ConfigParams.BAUDRATE_LENGTH:
            logger.error('数据长度不足，无法提取波特率')
            return None
        baudrate_bytes = data[ConfigParams.BAUDRATE_START:ConfigParams.BAUDRATE_START + ConfigParams.BAUDRATE_LENGTH]
        # 这里需要根据实际的转换逻辑将字节转换为波特率值
        baudrate = int.from_bytes(baudrate_bytes, byteorder='little')
        return baudrate

    @staticmethod
    def _extract_request_id(data):
        '''
        提取请求 ID
        :param data: 配置数据
        :return: 请求 ID 的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.REQUEST_ID_START + ConfigParams.REQUEST_ID_LENGTH:
            logger.error('数据长度不足，无法提取请求 ID')
            return None
        request_id_bytes = data[ConfigParams.REQUEST_ID_START:ConfigParams.REQUEST_ID_START + ConfigParams.REQUEST_ID_LENGTH]
        request_id = int.from_bytes(request_id_bytes, byteorder='little')
        return request_id

    @staticmethod
    def _extract_response_id(data):
        '''
        提取响应 ID
        :param data: 配置数据
        :return: 响应 ID 的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.RESPONSE_ID_START + ConfigParams.RESPONSE_ID_LENGTH:
            logger.error('数据长度不足，无法提取响应 ID')
            return None
        response_id_bytes = data[ConfigParams.RESPONSE_ID_START:ConfigParams.RESPONSE_ID_START + ConfigParams.RESPONSE_ID_LENGTH]
        response_id = int.from_bytes(response_id_bytes, byteorder='little')
        return response_id

    @staticmethod
    def _extract_get_key_status(data):
        '''
        提取获取密钥状态 DID
        :param data: 配置数据
        :return: 获取密钥状态 DID 的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.GET_KEY_STATUS_START + ConfigParams.GET_KEY_STATUS_LENGTH:
            logger.error('数据长度不足，无法提取获取密钥状态 DID')
            return None
        get_key_status_bytes =  data[ConfigParams.GET_KEY_STATUS_START:ConfigParams.GET_KEY_STATUS_START + ConfigParams.GET_KEY_STATUS_LENGTH]
        get_key_status = int.from_bytes(get_key_status_bytes, byteorder='little')
        return get_key_status

    @staticmethod
    def _extract_read_write_key(data):
        '''
        提取读写 DID
        :param data: 配置数据
        :return: 读写 DID 的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.READ_WRITE_KEY_START + ConfigParams.READ_WRITE_KEY_LENGTH:
            logger.error('数据长度不足，无法提取读写 DID')
            return None
        read_write_key_bytes = data[ConfigParams.READ_WRITE_KEY_START:ConfigParams.READ_WRITE_KEY_START + ConfigParams.READ_WRITE_KEY_LENGTH]
        read_write_key = int.from_bytes(read_write_key_bytes, byteorder='little')
        return read_write_key

    @staticmethod
    def _extract_nm_enabled(data):
        '''
        提取网络管理使能状态
        :param data: 配置数据
        :return: 网络管理使能状态的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.NM_ENABLED_START + ConfigParams.NM_ENABLED_LENGTH:
            logger.error('数据长度不足，无法提取网络管理使能状态')
            return None
        nm_enabled_byte = data[ConfigParams.NM_ENABLED_START:ConfigParams.NM_ENABLED_START + ConfigParams.NM_ENABLED_LENGTH]
        # 假设 0x01 表示 True，0x00 表示 False
        nm_enabled = bool(int.from_bytes(nm_enabled_byte, byteorder='little'))
        return nm_enabled

    @staticmethod
    def _extract_nm_id(data):
        '''
        提取网络管理报文 ID
        :param data: 配置数据
        :return: 网络管理报文 ID 的字节数据，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.NM_ID_START + ConfigParams.NM_ID_LENGTH:
            logger.error('数据长度不足，无法提取网络管理报文 ID')
            return None
        nm_id_bytes = data[ConfigParams.NM_ID_START:ConfigParams.NM_ID_START + ConfigParams.NM_ID_LENGTH]
        nm_id = int.from_bytes(nm_id_bytes, byteorder='little')
        return nm_id

    @staticmethod
    def _extract_nm_period(data):
        '''
        提取网络管理报文周期
        :param data: 配置数据
        :return: 网络管理报文周期的整数值，如果数据长度不足则返回 None
        '''
        if len(data) < ConfigParams.NM_PERIOD_START + ConfigParams.NM_PERIOD_LENGTH:
            logger.error('数据长度不足，无法提取网络管理报文周期')
            return None
        nm_period_bytes = data[ConfigParams.NM_PERIOD_START:ConfigParams.NM_PERIOD_START + ConfigParams.NM_PERIOD_LENGTH]
        nm_period = int.from_bytes(nm_period_bytes, byteorder='little')
        return nm_period
    
    def __str__(self):
        return f'数据：{utils.byte_array_to_hex_string(self.data)}'

if __name__ == '__main__':
#     config, result = ConfigParams.from_toml_data('tool-config.toml')
#     print(config)
#     print(result)
#     print(ConfigParams.to_config_str(config.data))
#     print('start')
#     # print(utils.byte_array_to_hex_string(utils.ascii_to_array('ABCDEF')))
    data_type = ValidValues.DATA_TYPE_RESPONSE
    command = ValidValues.COMMANDS_GET_KEY_STATUS
    data = b'\x11\x11\x11\x11\x11\x00\x00\x00\x00\x00'
    message = SerialMessage.generate_new_message(data_type, command, data)
    print(message)
    print(message.to_key_status())

#     message2 = SerialMessage.from_serial_data(message.full_data)
#     print(message2)

#     print('end')

#     '''
#     start
#     03-05 14:41:12.025 [DEBUG] [data_processor.py:119] Generate serial data: [4c 75 78 00 00 01 0a 00 41 42 43 44 45 46 47 48 49 50 11 0d 0a]       
#     原始数据：b'Lux\x00\x00\x01\n\x00ABCDEFGHIP\x11\r\n'
#     数据类型：0x00 请求，命令：0x0001 读取软件版本号，数据：41424344454647484950（ASCII：ABCDEFGHIP）)
#     03-05 14:41:12.026 [DEBUG] [data_processor.py:43] Received serial data: [4c 75 78 00 00 01 0a 00 41 42 43 44 45 46 47 48 49 50 11 0d 0a]        
#     原始数据：b'Lux\x00\x00\x01\n\x00ABCDEFGHIP\x11\r\n'
#     数据类型：0x00 请求，命令：0x0001 读取软件版本号，数据：41424344454647484950（ASCII：ABCDEFGHIP）)
#     end
#     '''