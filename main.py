from utils.logger import delete_expired_logs

import sys
import argparse  # 导入 argparse 模块

from PySide6.QtWidgets import QApplication

from utils.file_utils import read_file, resource_path

# 获取panel目录的路径
panel_dir = resource_path('panel')
sys.path.append(panel_dir)

from controller import Controller
# 定义 QSS 路径常量
BASIC_MAIN_QSS_PATH = resource_path('panel/basic_main_window.qss')
CONFIG_EDIT_QSS_PATH = resource_path('panel/config_edit.qss')
NO_CONFIG_FILE = 'NO_CONFIG_FILE'

if __name__ == '__main__':
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description='密钥下载工具配置')
    parser.add_argument('--open-config-edit', nargs='?', const=NO_CONFIG_FILE, help='仅打开 config_edit 界面，可选配置文件地址')
    args = parser.parse_args()
    
    # 打印解析后的参数，用于调试
    # print(f"解析后的参数: {args}")

    # 在程序开始时删除过期日志，如果注释这句不删除过期log需要注意全局log配置的过期时间
    delete_expired_logs()

    app = QApplication(sys.argv)

    controller = Controller(resource_path('panel/imgs/icon (2).png'), '密钥下载工具配置')
    controller.view.config_edit_qss = CONFIG_EDIT_QSS_PATH

    if args.open_config_edit:
        if args.open_config_edit == NO_CONFIG_FILE:
            # 不带路径，open_config_edit 不带参数
            controller.view.open_config_edit()
        else:
            # 带路径，参数传入 open_config_edit
            controller.view.open_config_edit(args.open_config_edit)
    else:
        # 正常打开主界面
        qssStyle = read_file(BASIC_MAIN_QSS_PATH)
        controller.view.setStyleSheet(qssStyle)

        controller.show_view()
    

    sys.exit(app.exec())
