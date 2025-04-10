from PySide6.QtWidgets import QComboBox
from PySide6.QtGui import QFontMetrics
#导入串口模块
from utils.serial_handle import SerialOperator
import logging

logger = logging.getLogger(__name__)

class MyComboBoxControl(QComboBox):

    def __init__(self, parent = None):
        super(MyComboBoxControl,self).__init__(parent) #调用父类初始化方法

    # 重写showPopup函数
    def showPopup(self):  
        # 获取原选项
        index = self.currentIndex()
        logger.debug('当前索引:%d', index)
        font_metrics = QFontMetrics(self.font())
        # 先清空原有的选项
        self.clear()
        # 初始化串口列表
        available_ports = SerialOperator().list_available_ports(True)
        logger.info('可用串口:%s', available_ports)
        # 计算滚动条宽度
        scrollbar_width = self.view().verticalScrollBar().sizeHint().width()
        # 计算视图的内边距
        view_margins = self.view().contentsMargins()
        total_margin_width = view_margins.left() + view_margins.right()
        max_width = 0
        for port in available_ports:
            self.addItem(port)

            # width = font_metrics.horizontalAdvance (port) + 30
            # 计算文本的宽度
            text_width = font_metrics.horizontalAdvance(port)
            # 计算包含滚动条和内边距的总宽度
            width = text_width + scrollbar_width + total_margin_width + 10
            if width > max_width:
                max_width = width

        if max_width > self.maximumWidth():
            self.view().setFixedWidth(max_width)

        if self.count() >= index:
            self.setCurrentIndex(index)
            logger.debug('重置串口数据，设置索引:%d', index)
        QComboBox.showPopup(self)   # 弹出选项框  


 
