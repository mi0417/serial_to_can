'''
    通用的数据处理
'''
import logging
import datetime
import re

logger = logging.getLogger(__name__)

def hex_str_to_little_endian_array(hex_str, byte_count=0):
    '''
    将十六进制字符串转换为小端字节数组。

    Args:
        hex_str (str): 十六进制字符串，如 '12345678'

    Returns:
        bytes: 小端字节数组，如 b'\x78\x56\x34\x12'
    '''
    # 移除可能存在的 '0x' 前缀
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]

    # 验证输入是否为有效的十六进制字符串
    if not all(c in '0123456789abcdefABCDEF ' for c in hex_str):
        return None
    
    # 将十六进制字符串转换为字节数组
    try:
        byte_array = bytes.fromhex(hex_str)
    except ValueError as e:
        logger.error('Invalid hex string: %s', e)
        return None
    
    # 反转字节数组以实现小端序
    little_endian_array = byte_array[::-1]

    # 如果指定了字节数，不足则补零
    if byte_count != 0:
        current_length = len(little_endian_array)
        if current_length < byte_count:
            padding = b'\x00' * (byte_count - current_length)
            little_endian_array = little_endian_array + padding
        elif current_length > byte_count:
            logger.warning('Byte count is smaller than the actual length of the array. Truncating.')
            little_endian_array = little_endian_array[:byte_count]

    return little_endian_array

def hex_str_to_byte_array(hex_str):
    '''
    将十六进制字符串转换为字节数组。

    Args:
        hex_str (str): 十六进制字符串，如 '12345678'

    Returns:
        bytes: 字节数组，如 b'\x12\x34\x56\x78'
    '''
    # 移除可能存在的 '0x' 前缀
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]

    # 验证输入是否为有效的十六进制字符串
    if not all(c in '0123456789abcdefABCDEF ' for c in hex_str):
        return None
    
    # 将十六进制字符串转换为字节数组
    try:
        byte_array = bytes.fromhex(hex_str)
    except ValueError as e:
        logger.error('Invalid hex string: %s', e)
        return None
    
    return byte_array

def little_endian_array_to_hex_str(byte_array):
    '''
    将小端字节数组转换为十六进制字符串。

    Args:
        byte_array (bytes): 小端字节数组，如 b'\x78\x56\x34\x12'

    Returns:
        str: 十六进制字符串，如 '12345678'
    '''
    if not isinstance(byte_array, (bytes, bytearray)):
        # 可以选择抛出异常，也可以返回 None
        # raise TypeError(f'Expected bytes or bytearray, got {type(byte_array).__name__}')
        logger.error('Invalid byte array: %s', byte_array)
        return None
    # 反转字节数组以恢复原始顺序
    original_array = byte_array[::-1]
    # 将字节数组转换为十六进制字符串
    hex_str = original_array.hex()
    return hex_str

def ascii_to_little_endian_array(ascii_str):
    '''
    将 ASCII 字符串转换为小端字节数组。

    Args:
        ascii_str (str): ASCII 字符串

    Returns:
        bytes: 小端字节数组
    '''
    try:
        byte_array = ascii_str.encode('ascii')
    except UnicodeEncodeError as e:
        logger.error('Encoding error: %s', e)
        return None
    little_endian_array = byte_array[::-1]
    return little_endian_array

def little_endian_array_to_ascii(byte_array):
    '''
    将小端字节数组转换为 ASCII 字符串。

    Args:
        byte_array (bytes): 小端字节数组

    Returns:
        str: ASCII 字符串
    '''
    if not isinstance(byte_array, (bytes, bytearray)):
        # 可以选择抛出异常，也可以返回 None
        # raise TypeError(f'Expected bytes or bytearray, got {type(byte_array).__name__}')
        logger.error('Invalid byte array: %s', byte_array)
        return None
    original_array = byte_array[::-1]
    ascii_str = original_array.decode('ascii')
    return ascii_str

def ascii_to_array(ascii_str):
    '''
    将 ASCII 字符串转换为字节数组。（非小端，不倒置）

    Args:
        ascii_str (str): ASCII 字符串

    Returns:
        bytes: 字节数组
    '''
    try:
        byte_array = ascii_str.encode('ascii')
    except UnicodeEncodeError as e:
        logger.error('Encoding error: %s', e)
        return None
    return byte_array

def array_to_ascii(byte_array):
    '''
    将字节数组转换为 ASCII 字符串。（非小端，不转置）

    Args:
        byte_array (bytes): 字节数组

    Returns:
        str: ASCII 字符串
    '''
    try:
        ascii_str = byte_array.decode('ascii', errors='replace')
        # 保留换行符和回车符，其他控制字符替换为点
        ascii_str = ''.join(
            c if (ord(c) >= 32 or c in '\n\r\t')
            else '.' if ord(c) < 128  
            else '.' 
            for c in ascii_str
        )
        return ascii_str
    except Exception as e:
        logger.error('Decoding error: %s', e)
        return f"非ASCII数据: {e}"

def hex_to_ascii(hex_str):
    '''
    将十六进制字符串转换为 ASCII 字符串。

    Args:
        hex_str (str): 十六进制字符串

    Returns:
        str: ASCII 字符串
    '''
    try:
        if hex_str.startswith('0x'):
            hex_str = hex_str[2:]
        return bytes.fromhex(hex_str).decode('ascii')
    except UnicodeDecodeError as e:
        logger.error('Decoding error: %s', e)
        return None
    except ValueError as e:
        logger.error('Invalid hex string: %s', e)
        return None

def ascii_to_hex(ascii_str):
    '''
    将 ASCII 字符串转换为十六进制字符串。

    Args:
        ascii_str (str): ASCII 字符串

    Returns:
        str: 十六进制字符串
    '''
    try:
        return ascii_str.encode('ascii').hex()
    except UnicodeEncodeError as e:
        logger.error('Encoding error: %s', e)
        return None

def split_string(data, separator=','):
    '''
    将字符串按指定分隔符拆分为列表。

    :param data: 待拆分的字符串
    :param separator: 分隔符，默认为逗号
    :return: 拆分后的列表
    '''
    return data.split(separator)

def convert_to_int(data):
    '''
    尝试将数据转换为整数，转换失败则返回 None。

    :param data: 待转换的数据
    :return: 转换后的整数或 None
    '''
    try:
        return int(data)
    except ValueError:
        return None

def calculate_crc(data):
    '''
    计算 CRC 校验码。

    :param data: 待计算 CRC 的数据
    :return: CRC 校验码 int类型
    '''
    if not hasattr(data, '__iter__'):
        logger.error('Invalid input: data must be an iterable object.')
        return None
    check_sum = 0
    for item in data:
        if not isinstance(item, int):
            logger.error('Invalid element in data: all elements must be integers.')
            return None
        check_sum ^= item
    return check_sum

def calculate_crc_bytes(data):
    '''
    计算 CRC 校验码，并将结果转换为字节数组。

    :param data: 待计算 CRC 的数据
    :return: CRC 校验码的字节数组
    '''
    crc = calculate_crc(data)
    if crc is None:
        return None
    return crc.to_bytes(1, byteorder='little', signed=False)

def byte_array_to_hex_string(byte_array):
    '''
    将字节数组转换为 XX XX XX 格式的十六进制字符串。

    Args:
        byte_array (bytes): 字节数组

    Returns:
        str: XX XX XX 格式的十六进制字符串
    '''
    if not isinstance(byte_array, (bytes, bytearray)):
        logger.error('Invalid byte array: %s', byte_array)
        return None
    hex_str = byte_array.hex()
    # 在每两个字符之间插入空格
    formatted_hex_str = ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
    return formatted_hex_str

def byte_array_to_hex_string_with_newline(byte_array):
    '''
    将字节数组转换为 XX XX XX 格式的十六进制字符串，
    若长度超过 8 位，每 8 位添加一个换行符。

    Args:
        byte_array (bytes): 字节数组

    Returns:
        str: 格式化后的十六进制字符串
    '''
    formatted_hex_str = byte_array_to_hex_string(byte_array)
    if formatted_hex_str is None:
        return None
    
    parts = []
    for i in range(0, len(formatted_hex_str), 24):  # 每 8 个十六进制数（包含 7 个空格）长度为 23
        parts.append(formatted_hex_str[i:i+24])
    return '\n'.join(parts)

def int_to_fixed_bytes(num, length):
    '''
    将整数转换为固定长度的小端字节数组。

    Args:
        num (int): 要转换的整数。
        length (int): 期望的字节数组长度。

    Returns:
        bytes: 固定长度的小端字节数组。
    '''
    try:
        # 将整数转换为字节数组
        byte_array = num.to_bytes(length, byteorder='little')
        return byte_array
    except OverflowError:
        logger.error('整数 %d（%s） 无法用 %d 字节表示。', num, hex(num), length)
        return None
    
def int_to_hex_string(num: int) -> str:
    """
    将整数转换为以 0x 开头，后面为大写形式的十六进制字符串。

    :param num: 要转换的整数
    :return: 转换后的十六进制字符串
    """
    hex_str = hex(num)
    return "0x" + hex_str[2:].upper()
    
def format_timestamp(timestamp):
    """
    将时间戳转换为格式化的字符串。

    :param timestamp: 时间戳，单位为秒
    :return: 格式化后的字符串，格式为 'YYYY-MM-DD HH:MM:SS.fff'
    """
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    formatted_time = dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return formatted_time

def split_hex_string(input_string):
    """
    将输入的字符串拆分为最长 2 位的十六进制数组，若元素只有一位则补零。

    :param input_string: 包含十六进制数字的字符串，数字可能以逗号、空格或其他符号分隔
    :return: 拆分后的十六进制数组
    """
    # 先使用正则表达式提取所有可能的十六进制片段
    hex_segments = re.findall(r'[0-9a-fA-F]+', input_string)
    result = []
    for segment in hex_segments:
        # 按每 2 个字符分割当前片段
        for i in range(0, len(segment), 2):
            hex_part = segment[i:i + 2]
            # 若长度为 1 则补零
            if len(hex_part) == 1:
                hex_part = '0' + hex_part
            result.append(hex_part)
    return result

def split_hex_string_to_byte_array(input_string):
    """
    将以空格、换行等分隔的包含十六进制数字的字符串转换为字节数组。

    :param input_string: 包含十六进制数字的字符串，数字可能以空格、换行或其他符号分隔
    :return: 转换后的字节数组，如果输入无效则返回 None
    """
    # 先使用正则表达式提取所有可能的十六进制片段
    hex_segments = re.findall(r'[0-9a-fA-F]+', input_string)
    hex_str = ""
    for segment in hex_segments:
        # 按每 2 个字符分割当前片段
        for i in range(0, len(segment), 2):
            hex_part = segment[i:i + 2]
            # 若长度为 1 则补零
            if len(hex_part) == 1:
                hex_part = '0' + hex_part
            hex_str += hex_part
    try:
        # 将组合后的十六进制字符串转换为字节数组
        return bytes.fromhex(hex_str)
    except ValueError:
        logger.error('Invalid hex string: %s', input_string)
        return None

class CommentParser:
    """处理Python代码中的注释，支持多行字符串
    """
    # # 使用示例
    # parser = CommentParser()
    # lines = [
    #     'def func():\n',
    #     '    """这是一个文档字符串',
    #     '    包含#符号但不是注释',
    #     '    """',
    #     '    ',
    #     '    print("# 这也不是注释")  # 这才是注释',
    #     '# 这是行首注释'
    # ]
    # for line in lines:
    #     leading_whitespace, code, comment = parser.split_code_and_comment_with_whitespace(line)
    #     print(f"行 {parser.current_line}: 前导='{leading_whitespace}', 代码='{code}', 注释='{comment}', 状态={parser.state}")
    
    STATE_SINGLE_QUOTE = 'single_quote'
    STATE_DOUBLE_QUOTE = 'double_quote'
    STATE_TRIPLE_SINGLE = 'triple_single'   # 三个单引号
    STATE_TRIPLE_DOUBLE = 'triple_double'

    def __init__(self):
        # 解析状态：None, 'single_quote', 'double_quote', 'triple_single', 'triple_double'
        self.state = None
        self.current_line = 0
    
    def split_code_and_comment_with_whitespace(self, line: str) -> tuple[str, str, str]:
        """
        分离单行代码和注释，维护多行状态
        返回：(代码部分, 注释部分)
        """
        self.current_line += 1
        line = line.rstrip('\n')
        leading_whitespace = ""
        content = ""
        comment = ""
        
        # 提取行首的空白字符
        for char in line:
            if char in (' ', '\t'):
                leading_whitespace += char
            else:
                break
        line = line[len(leading_whitespace):]  # 去掉行首空白字符后的剩余内容

        i = 0
        length = len(line)
        
        while i < length:
            char = line[i]
            
            # 检查是否在三引号字符串中结束
            if self.state in [self.STATE_TRIPLE_SINGLE, self.STATE_TRIPLE_DOUBLE]:
                quote = "'''" if self.state == self.STATE_TRIPLE_SINGLE else '"""'
                if i <= length - 3 and line[i:i+3] == quote:
                    self.state = None
                    i += 3
                    continue
            
            
            # 检查是否在单引号/双引号字符串中结束
            elif self.state in [self.STATE_SINGLE_QUOTE, self.STATE_DOUBLE_QUOTE]:
                quote_char = "'" if self.state == self.STATE_SINGLE_QUOTE else '"'
                if char == quote_char:
                    # 检查是否为转义的引号
                    escaped = i > 0 and line[i - 1] == '\\'
                    # 处理奇数个转义字符的情况
                    escape_count = 0
                    j = i - 1
                    while j >= 0 and line[j] == '\\':
                        escape_count += 1
                        j -= 1
                    if escape_count % 2 == 0:  # 偶数个转义字符，说明引号是真正的结束
                        self.state = None
                    if not escaped:
                        i += 1
                        continue
            
            # 当前不在任何字符串中，检查新的字符串或注释
            if self.state is None:
                # 检查三引号字符串开始
                if i <= length - 3 and line[i:i+3] in ['"""', "'''"]:
                    quote = line[i:i+3]
                    self.state = self.STATE_TRIPLE_SINGLE if quote == "'''" else self.STATE_TRIPLE_DOUBLE
                    i += 3
                    continue
                
                # 检查单引号/双引号字符串开始
                if char in ["'", '"']:
                    # 检查是否为转义的引号
                    if i > 0 and line[i - 1] == '\\':
                        i += 1
                        continue
                    self.state = self.STATE_SINGLE_QUOTE if char == "'" else self.STATE_DOUBLE_QUOTE
                    i += 1
                    continue
                
                # 检查注释
                if char == '#':
                    comment_start = i
                    code_end = comment_start - 1
                    while code_end >= 0 and line[code_end].isspace():
                        code_end -= 1
                    
                    content = line[:code_end + 1]
                    comment = line[code_end + 1:]
                    break
                
            i += 1
        if not content and not comment:
            content = line

        return leading_whitespace, content, comment

    def split_code_and_comment(self, line: str) -> tuple[str, str]:
        """
        分离代码和注释（不含空格）
        返回：(代码部分, 注释部分)
        """
        leading_whitespace, code_part, comment_part = self.split_code_and_comment_with_whitespace(line)
        # 移除注释前的所有空格
        comment_part = comment_part.lstrip()
        return code_part, comment_part