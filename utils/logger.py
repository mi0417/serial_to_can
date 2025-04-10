'''
    日志模块
'''
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import datetime

LOG_DIR = './save_data'
BACKUP_DAY = 7

def configure_logger(path=LOG_DIR, backup_day=BACKUP_DAY):
    # 创建根 logger
    # 创建一个模块级别的日志记录器
    root_logger = logging.getLogger()

    # 配置日志记录器
    # logger.setLevel(logging.INFO)
    root_logger.setLevel(logging.DEBUG)

    # 当前日期
    current_date = datetime.date.today()
    formatted_date = current_date.strftime('%Y%m%d')

    if not os.path.exists(path):
        os.makedirs(path)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)       

    # 创建一个按天切割的文件处理器，保存debug级的log
    file_handler = TimedRotatingFileHandler(
        filename=f'{path}/app_{formatted_date}_debug.log',
        when='D',  # 按天切割
        interval=1,  # 每天切割一次
        backupCount=backup_day,  # 保留最近 7 天的日志文件
        encoding='utf-8'  # 指定日志文件编码为 UTF-8
    )
    file_handler.setLevel(logging.DEBUG)

    # 创建一个按天切割的文件处理器，保存info级的log
    file_handler_info = TimedRotatingFileHandler(
        filename=f'{path}/app_{formatted_date}_info.log',
        when='D',  # 按天切割
        interval=1,  # 每天切割一次
        backupCount=backup_day,  # 保留最近 7 天的日志文件
        encoding='utf-8'  # 指定日志文件编码为 UTF-8
    )
    file_handler_info.setLevel(logging.INFO)

    # 创建一个格式化器，用于设置日志消息的格式
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)7s] [%(filename)16s:%(lineno)-3d] %(message)s',
                        datefmt = '%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    formatter = logging.Formatter('%(asctime)s - %(name)20s - %(levelname)7s - [%(filename)16s:%(lineno)-3d] - %(message)s')
    file_handler.setFormatter(formatter)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler_info.setFormatter(formatter)

    # 将处理程序添加到日志记录器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(file_handler_info)

    # logging.basicConfig(format = '%(asctime)s.%(msecs)03d [%(levelname)-7s] [%(filename)16s:%(lineno)-3d] %(message)s',
    #                     datefmt = '%m-%d %H:%M:%S')
    return root_logger

global_logger = configure_logger()

# 删除过期日志文件
def delete_expired_logs(log_dir=LOG_DIR, backup_count=BACKUP_DAY):
    # 获取当前日期
    current_date = datetime.date.today()
    # 计算需要删除的日期
    expired_date = current_date - datetime.timedelta(days=backup_count)
    # 列出日志目录下的所有文件
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
    for log_file in log_files:
        # 假设日志文件名包含日期信息，格式为 YYYYMMDD
        try:
            file_date_str = log_file.split('_')[1].split('.')[0]
            file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d').date()
            if file_date < expired_date:
                # 删除过期的日志文件
                global_logger.info('Delete expired log file: %s', log_file)
                os.remove(os.path.join(log_dir, log_file))
        except (IndexError, ValueError):
            # 处理文件名格式不符合预期的情况
            continue 