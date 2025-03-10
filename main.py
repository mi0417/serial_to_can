import sys
from PySide6.QtWidgets import QApplication
from controller import Controller

from file_utils import read_file, resource_path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller(resource_path("imgs/icon (2).png"), '密钥下载工具配置')
    qssStyle = read_file(resource_path('basic_main_window.qss'))
    controller.view.setStyleSheet(qssStyle)
    controller.show_view()
    sys.exit(app.exec())
