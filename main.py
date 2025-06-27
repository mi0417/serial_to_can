from utils.logger import delete_expired_logs

import sys
from PySide6.QtWidgets import QApplication

from utils.file_utils import read_file, resource_path

from controller import Controller

if __name__ == '__main__':

    # 在程序开始时删除过期日志，如果注释这句不删除过期log需要注意全局log配置的过期时间
    delete_expired_logs()

    app = QApplication(sys.argv)
    controller = Controller(resource_path('panel/imgs/icon (2).png'), '密钥下载工具配置')
    qssStyle = read_file(resource_path('panel/basic_main_window.qss'))
    controller.view.setStyleSheet(qssStyle)
    controller.show_view()
    sys.exit(app.exec())
