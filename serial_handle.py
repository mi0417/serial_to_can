'''
    串口操作类
'''
import serial
import serial.tools.list_ports

from logger import logger
from common_data_utils import byte_array_to_hex_string

class SerialOperator:
    '''
    串口操作类
    '''
    def __init__(self):
        self.id = id(self)
        self._ser = None
        self._is_open = False
        self._opened_port = None

    def __del__(self):
        self.close_serial_port()

    @property
    def port(self):
        '''
        获取当前打开的串口名称。

        :return: 当前打开的串口名称，如果没有打开串口，则返回 None
        '''
        return self._opened_port
    
    @property
    def is_open(self):
        '''
        获取当前串口是否打开的状态，并检查串口是否断开。

        :return: 如果串口已打开，返回 True；否则返回 False
        '''
        return self._is_open

    
    def list_available_ports(self, description=False):
        '''
        获取可用的串口列表及其详细信息。

        :param description: 可选参数，用于过滤串口描述信息。如果提供了该参数，
                            则只返回描述信息中包含该参数的串口信息。'

        :return: 一个包含串口信息的列表，每个元素是一个字典，包含以下键值对：
                 - 'device': 串口号，例如 'COM3' 或 '/dev/ttyUSB0'
                 - 'name': 串口名称
                 - 'description': 串口描述信息
        '''
        ports = serial.tools.list_ports.comports()
        if description:
            return [f'{port.device} #{port.description}' for port in ports]
        else:
            return [port.device for port in ports]


    def open_serial_port(self, port:str, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=1):
        '''
        打开指定的串口。如果该串口已经打开，则先关闭它再重新打开。

        :param port: 要打开的串口号，例如 'COM3' 或 '/dev/ttyUSB0'
        :param baudrate: 串口通信的波特率，默认为 115200
        :param bytesize: 串口数据位，默认为 8 位
        :param stopbits: 串口停止位，默认为 1 位
        :param timeout: 串口操作的超时时间，单位为秒，默认为 1 秒
        :return: 若成功打开串口，返回 True；若打开失败，返回 False
        '''
        # 提取实际的串口设备名
        port_name = port.split(' #')[0]
        if self._is_open and self._opened_port == port_name:
            logger.debug('串口 %s 已经打开', port_name)
            # 如果该实体已经打开了这个串口，无需重复操作
            return True
        try:
            if self._is_open:
                # 如果该实体已经打开了其他串口，先关闭它
                self.close_serial_port()
            self._ser = serial.Serial(port_name, baudrate, bytesize=bytesize, stopbits=stopbits, timeout=timeout, write_timeout=timeout)
            # 检查串口是否成功打开
            if self._ser.is_open:
                logger.info('成功打开串口: %s', port_name)
                self._is_open = True
                self._opened_port = port_name
                return True
            else:
                logger.info('打开串口 %s 失败', port_name)
                return False
        except serial.SerialException as e:
            logger.error('打开串口 %s 失败: %s', port_name, e)
            return False
        

    def close_serial_port(self):
        if self._ser and self._is_open:
            self._ser.close()
            logger.info('串口%s已关闭', self._opened_port)
        else:
            logger.debug('没有打开的串口')
        self._is_open = False
        self._opened_port = None

    def send_data(self, data):
        if self._ser and self._ser.is_open:
            if isinstance(data, str):
                data = data.encode()
            try:
                bytes_sent = self._ser.write(data)
                logger.info('已发送 %d 字节数据: [%s]', bytes_sent, byte_array_to_hex_string(data))
                return bytes_sent
            except serial.SerialException as e:
                logger.error('发送数据时出错: %s，尝试重新开关串口', e)
                self.serial_reopen()
        return 0

    def receive_data(self, size=None):
        if self._ser and self._ser.is_open:
            try:
                if size is None:
                    data = self._ser.read(self._ser.in_waiting)
                else:
                    data = self._ser.read(size)
                if data:
                    logger.info('接收到 %d 字节数据: [%s]', len(data), byte_array_to_hex_string(data))
                return data
            except serial.SerialException as e:
                logger.error('接收数据时出错: %s，尝试重新开关串口', e)
                self.serial_reopen()
        return b''

    def serial_reopen(self):
        '''
        重新打开串口（收发异常时尝试）
        '''
        if self._ser and self._opened_port:
            port = self._opened_port
            self.close_serial_port()
            return self.open_serial_port(port)
        else:
            logger.debug('没有打开的串口')

# 假设要处理 2 个固定的串口
# if __name__ == '__main__':
#     available_ports = SerialOperator().list_available_ports()
#     logger.debug(f'可用串口:{available_ports}')

#     if len(available_ports) >= 2:
#         # 创建 2 个 SerialOperator 实例
#         serial_op1 = SerialOperator()
#         serial_op2 = SerialOperator()

#         # 打开指定的 2 个串口
#         port1 = available_ports[0]
#         port2 = available_ports[1]
#         serial_op1.open_serial_port(port1)
#         serial_op2.open_serial_port(port2)

#         # 向第一个串口发送数据
#         serial_op1.send_data('Hello, Serial 1!')

#         # 从第二个串口接收数据
#         received_data = serial_op2.receive_data()

#         # 关闭串口
#         serial_op1.close_serial_port()
#         serial_op2.close_serial_port()
