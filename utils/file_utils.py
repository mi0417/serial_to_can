import sys
import os
import toml

import logging

logger = logging.getLogger(__name__)

def resource_path(relative_path):
    ''' 一般用于内部资源文件 Get the absolute path to the resource, works for dev and for PyInstaller '''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


def exe_absolute_path(relative_path):
    '''一般用于外部配置文件，如果为绝对路径则不转换'''
    if os.path.isabs(relative_path):
        return relative_path
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

def is_file_exists(file_path):
    '''
    判断指定文件是否存在
    :param file_path: 文件的路径
    :return: 如果文件存在返回 True，否则返回 False
    '''
    return os.path.exists(file_path)

def is_file_exists(file_path):
    '''
    判断指定文件是否存在
    :param file_path: 文件的路径
    :return: 如果文件存在返回 True，否则返回 False
    '''
    try:
        exists = os.path.exists(file_path)
        if exists:
            logger.info(f'文件 {file_path} 存在。')
        else:
            logger.info(f'文件 {file_path} 不存在。')
        return exists
    except Exception as e:
        logger.error(f'检查文件 {file_path} 时出错: {e}')
        return False
    
def create_file(file_path):
    '''
    创建一个空文件，如果文件已存在则不做任何操作
    :param file_path: 文件的路径
    '''
    try:
        # 以写入模式打开文件，如果文件不存在会创建文件
        with open(file_path, 'w', encoding='utf-8') as file:
            pass
        logger.info('文件 %s 已成功创建。', file_path)
    except Exception as e:
        logger.error('创建文件 %s 时出错: %s', file_path, e)


def read_file(file_path):
    '''
    读取指定文件的内容
    :param file_path: 文件的路径
    :return: 文件内容，如果文件不存在则返回空字符串
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error('文件 %s 未找到。', file_path)
        return ''


def write_file(file_path, content):
    '''
    将指定内容写入文件，如果文件不存在则创建文件，如果文件已存在则覆盖原有内容
    :param file_path: 文件的路径
    :param content: 要写入的内容
    '''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        logger.info('内容已成功写入 %s。', file_path)
    except Exception as e:
        logger.error('写入文件 %s 时出错: %s', file_path, e)


def append_to_file(file_path, content):
    '''
    将指定内容追加到文件末尾，如果文件不存在则创建文件
    :param file_path: 文件的路径
    :param content: 要追加的内容
    '''
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)
        logger.info('内容已成功追加到 %s。', file_path)
    except Exception as e:
        logger.error('追加内容到文件 %s 时出错: %s', file_path, e)


def open_file(file_path, mode='r', encoding='utf-8'):
    '''
    打开文件并返回文件对象
    :param file_path: 文件的路径
    :param mode: 打开文件的模式，默认为 'r'（读取模式）
    :param encoding: 文件编码，默认为 'utf-8'
    :return: 文件对象
    '''
    try:
        file = open(file_path, mode, encoding=encoding)
        logger.info('文件 %s 已成功打开。', file_path)
        return file
    except Exception as e:
        logger.error('打开文件 %s 时出错: %s', file_path, e)
        return None


def close_file(file):
    '''
    关闭文件对象
    :param file: 文件对象
    '''
    if file:
        try:
            file.close()
            logger.info('文件已成功关闭。')
        except Exception as e:
            logger.error('关闭文件时出错: %s', e)

def read_toml_file(file_path):
    '''
    读取 TOML 文件内容
    :param file_path: TOML 文件的路径
    :return: 解析后的 TOML 数据，如果文件不存在或解析出错则返回空字典
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return toml.load(file)
    except FileNotFoundError:
        logger.info('文件 %s 未找到。', file_path)
        return {}
    except toml.TomlDecodeError as e:
        logger.error('解析 TOML 文件 %s 时出错: %s', file_path, e)
        return {}

def write_toml_file(file_path, data):
    '''
    将数据写入 TOML 文件，如果文件不存在则创建，如果文件已存在则覆盖原有内容
    :param file_path: TOML 文件的路径
    :param data: 要写入的 TOML 数据（字典形式）
    '''
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            toml.dump(data, file)
        logger.info('数据已成功写入 %s。', file_path)
    except Exception as e:
        logger.error('写入 TOML 文件 %s 时出错: %s', file_path, e)

def update_toml_file(file_path, new_data):
    '''
    更新 TOML 文件中的数据，如果文件不存在则创建并写入新数据
    :param file_path: TOML 文件的路径
    :param new_data: 要更新的新数据（字典形式）
    '''
    existing_data = read_toml_file(file_path)
    existing_data.update(new_data)
    write_toml_file(file_path, existing_data)
    logger.info('文件 %s 已成功更新。', file_path)