'''
    通用的数据处理
'''
from logger import logger

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
    if not all(c in '0123456789abcdefABCDEF' for c in hex_str):
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
    if not isinstance(byte_array, (bytes, bytearray)):
        # 可以选择抛出异常，也可以返回 None
        # raise TypeError(f'Expected bytes or bytearray, got {type(byte_array).__name__}')
        logger.error('Invalid byte array: %s', byte_array)
        return None
    ascii_str = byte_array.decode('ascii')
    return ascii_str

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
    except ValueError as e:
        logger.error('Invalid hex string: %s', e)
        return None
    except UnicodeDecodeError as e:
        logger.error('Decoding error: %s', e)
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
        logger.error(f'整数 {num}（{hex(num)}） 无法用 {length} 字节表示。')
        return None