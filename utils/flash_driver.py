'''
FlashDriver 业务处理模块

职责：FlashDriver 文件的读取、CRC32 计算、分片、配置解析
不依赖 UI 和 Controller，纯粹的工具层
'''
import os
import logging

import utils.common_data_utils as utils
import utils.file_utils as file_utils
from utils.data_processor import ValidValues

logger = logging.getLogger(__name__)

# 分片大小（从常量库取，不在本模块硬编码）
CHUNK_SIZE = ValidValues.MAX_APP_DATA_LENGTH


def get_file_path_from_config(config_path):
    '''
    从配置文件中读取 FlashDriver 文件名，并解析为完整路径

    :param config_path: 配置文件路径（TOML 格式）
    :return: 文件完整路径，读取失败或文件不存在返回 None
    '''
    section = ValidValues.FLASH_DRIVER_SECTION
    name_key = ValidValues.FLASH_DRIVER_NAME_KEY

    if not config_path or not file_utils.is_file_exists(config_path):
        return None

    try:
        config = file_utils.read_toml_file(config_path)
        if section in config:
            file_name = config[section].get(name_key)
            if file_name:
                full_path = _resolve_path(file_name, section)
                if file_utils.is_file_exists(full_path):
                    logger.info('从配置解析到 FlashDriver 路径: %s', full_path)
                    return full_path
    except Exception as e:
        logger.warning('从配置 %s 解析 FlashDriver 路径失败: %s', config_path, e)

    return None


def _resolve_path(file_name, section=None):
    '''
    根据文件名解析完整路径

    :param file_name: 文件名
    :param section: 目录名（默认为 section 名）
    :return: 文件的完整路径
    '''
    if section is None:
        section = ValidValues.FLASH_DRIVER_SECTION

    flash_driver_dir = os.path.join(file_utils.get_exe_dir(), section)

    # 1. 优先原文件名（用户可能手动改了文件名但没后缀）
    original_path = os.path.join(flash_driver_dir, file_name)
    if os.path.exists(original_path):
        logger.info('找到 FlashDriver 文件(原名): %s', original_path)
        return original_path

    # 2. 自动补 .bin 后缀
    if not file_name.lower().endswith('.bin'):
        bin_path = os.path.join(flash_driver_dir, file_name + '.bin')
        if os.path.exists(bin_path):
            logger.info('找到 FlashDriver 文件(补后缀): %s', bin_path)
            return bin_path

    # 3. 都找不到，返回原路径（让调用方处理）
    logger.warning('未找到 FlashDriver 文件: %s 或 %s',
                   original_path, bin_path if not file_name.lower().endswith('.bin') else 'N/A')
    return original_path


def read_flash_driver_file(file_path):
    '''
    读取 FlashDriver bin 文件

    :param file_path: 文件完整路径
    :return: 文件内容（bytes），读取失败返回 None
    '''
    if not file_utils.is_file_exists(file_path):
        logger.error('FlashDriver 文件不存在: %s', file_path)
        return None

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            logger.info('成功读取 FlashDriver 文件: %s (%d bytes)', file_path, len(data))
            return data
    except Exception as e:
        logger.error('读取 FlashDriver 文件 %s 失败: %s', file_path, e)
        return None


def calculate_flash_driver_crc32(data):
    '''
    计算 FlashDriver 数据的 CRC32（用于最终校验）

    :param data: bin 文件内容（bytes）
    :return: CRC32 值（int）
    '''
    crc = utils.calc_crc32(data)
    logger.debug('FlashDriver CRC32: 0x%08X', crc)
    return crc


def get_flash_driver_chunk(data, chunk_size, offset):
    '''
    按 offset 取指定分片数据

    :param data: 完整 bin 数据
    :param chunk_size: 每片大小
    :param offset: 目标偏移量
    :return: (offset, chunk_data) 或 None（越界）
    '''
    if offset >= len(data):
        return None
    chunk_data = data[offset:offset + chunk_size]
    return (offset, chunk_data)


def chunk_flash_driver_data(data, chunk_size=CHUNK_SIZE):
    '''
    将 FlashDriver 数据分片

    :param data: 完整 bin 数据
    :param chunk_size: 每片数据大小（字节）
    :return: list of (offset, chunk_data)
        offset: 数据偏移量（int）
        chunk_data: 当前片的数据（bytes）
    '''
    chunks = []
    offset = 0
    while offset < len(data):
        chunk_data = data[offset:offset + chunk_size]
        chunks.append((offset, chunk_data))
        offset += len(chunk_data)

    logger.info('FlashDriver 分片完成: %d 字节分为 %d 片，每片最大 %d 字节',
                len(data), len(chunks), chunk_size)
    return chunks


def validate_flash_driver_file(file_path):
    '''
    验证 FlashDriver 文件有效性
    未使用

    :param file_path: 文件路径
    :return: (is_valid, error_message)
    '''
    if not file_utils.is_file_exists(file_path):
        return False, '文件不存在'

    try:
        file_size = os.path.getsize(file_path)
        if file_size < 1:
            return False, f'文件大小 {file_size} 字节，无效'
        return True, None
    except Exception as e:
        return False, f'文件访问失败: {e}'


def get_flash_driver_info(file_path):
    '''
    获取 FlashDriver 文件的基本信息摘要
    没用

    :param file_path: 文件完整路径
    :return: dict 包含 size、crc32、chunks 等，失败返回 None
        {
            'file_path': str,
            'file_name': str,
            'size': int,
            'crc32': int,
            'chunks': list of (offset, chunk_data),
            'chunks_count': int,
            'chunk_size': int,
        }
    '''
    data = read_flash_driver_file(file_path)
    if data is None:
        return None

    info = {
        'file_path': file_path,
        'file_name': os.path.basename(file_path),
        'size': len(data),
        'crc32': calculate_flash_driver_crc32(data),
        'chunks': chunk_flash_driver_data(data, CHUNK_SIZE),
        'chunks_count': 0,
        'chunk_size': CHUNK_SIZE,
    }
    info['chunks_count'] = len(info['chunks'])
    return info