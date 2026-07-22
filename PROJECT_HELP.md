# 串口转CAN工具 - 项目帮助文档

## 文档版本
- **版本**: V1.0
- **更新日期**: 2026-07-06
- **项目名称**: SerialToCAN (密钥下载工具配置)

---

## 一、项目概述

### 1.1 项目定位
这是一个**上位机工具**，用于通过串口与嵌入式设备（黑盒子）通信，实现：
- 设备配置参数的下发与读取
- 密钥（FlashDriver）下载到设备
- Qi 无线充电密钥的写入
- 设备状态监控

### 1.2 技术架构
```
┌─────────────────────────────────────────────────────────────┐
│                     上位机 (Python + PySide6)               │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  View   │◄──►│ Controller  │◄──►│       Model         │ │
│  │  界面层  │    │   控制层     │    │ 业务逻辑/数据处理    │ │
│  └─────────┘    └──────┬──────┘    └──────────┬──────────┘ │
│                        │                       │            │
│                        ▼                       ▼            │
│              ┌─────────────────┐     ┌─────────────────┐   │
│              │ SerialHandle    │     │ DataProcessor   │   │
│              │ 串口通信封装     │     │ 串口协议解析     │   │
│              └─────────────────┘     └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼ 串口 RS232/RS485
┌─────────────────────────────────────────────────────────────┐
│                  下位机 (NXP S32K312 嵌入式)                │
│  - UDS 诊断协议                                              │
│  - CAN/CANFD/LIN/Uart 通信                                  │
│  - 密钥存储管理                                              │
│  - FlashDriver OTA                                          │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 项目目录结构
```
SerialToCAN/
├── main.py                 # 程序入口
├── controller.py           # 控制器（MVC核心）
├── model.py                # 业务模型
├── tool-config.toml        # 默认配置文件
│
├── config/                 # 配置模块
│   └── api_config.py       # API服务器配置
│
├── view/                   # 视图层
│   ├── view.py             # 主窗口
│   ├── config_edit.py      # 配置编辑窗口
│   └── login_dialog.py     # 登录对话框
│
├── utils/                  # 工具层
│   ├── serial_handle.py    # 串口操作封装
│   ├── data_processor.py   # 串口协议/配置解析
│   ├── api_client.py       # Qi密钥服务器API客户端
│   ├── flash_driver.py     # FlashDriver文件处理
│   ├── file_utils.py       # 文件操作工具
│   ├── common_data_utils.py# 通用数据转换工具
│   └── logger.py           # 日志配置
│
├── panel/                  # UI资源
│   ├── basic_main_window.ui       # 主窗口UI
│   ├── config_edit.ui             # 配置编辑UI
│   ├── *.qss                       # 样式文件
│   └── imgs/                       # 图片资源
│
└── output/                 # 输出目录
    ├── FlashDriver/        # FlashDriver文件存放
    └── tool-config-*.toml  # 生成的配置文件
```

---

## 二、核心模块详解

### 2.1 入口模块 (main.py)

**文件路径**: `main.py`

**功能职责**:
- 程序启动入口
- 命令行参数解析
- 界面初始化与启动

**关键代码逻辑**:
```python
# 支持的命令行参数
--open-config-edit [配置文件路径]  # 仅打开配置编辑界面
```

**修改指引**:
- 添加新命令行参数：在 `argparse` 部分添加
- 修改启动流程：修改 `if __name__ == '__main__'` 块

---

### 2.2 控制器层 (controller.py)

**文件路径**: `controller.py`

**功能职责**:
- 协调 View 和 Model 的交互
- 管理串口通信线程
- 处理用户操作和业务逻辑流程

**核心类**:

#### Controller
主控制器类，负责整体业务协调。

| 方法 | 功能说明 |
|------|----------|
| `toggle_serial()` | 连接/断开串口 |
| `get_software_version()` | 获取设备软件版本 |
| `reset_device()` | 复位设备 |
| `set_config_device()` | 配置设备参数 |
| `read_config_device()` | 读取设备配置 |
| `one_key_config()` | 一键配置（配置→读取确认→下载FlashDriver） |
| `get_key_status()` | 获取密钥状态 |
| `input_flash_driver()` | 下载 FlashDriver |
| `get_uid()` | 获取设备 UID |
| `write_qi_key()` | 写入 Qi 密钥 |
| `send_flash_driver()` | 触发 FlashDriver 传输 |

#### SerialCommunicationThread
串口通信子线程，处理所有串口相关操作。

| 信号 | 说明 |
|------|------|
| `result_signal` | 串口打开结果 |
| `data_received` | 收到数据 |
| `sw_ver_signal` | 软件版本号 |
| `serial_closed_signal` | 串口关闭通知 |
| `reset_result_signal` | 复位结果 |
| `set_config_result_signal` | 配置结果 |
| `read_config_result_signal` | 读取配置结果 |
| `get_key_status_result_signal` | 密钥状态结果 |
| `input_flash_driver_result_signal` | FlashDriver下载结果 |
| `get_uid_result_signal` | UID读取结果 |
| `write_qi_key_result_signal` | Qi密钥写入结果 |
| `send_flash_driver_result_signal` | FlashDriver传输结果 |

**修改指引**:
- 添加新功能：在 `Controller` 中添加方法，连接相应的 View 信号
- 修改业务逻辑：在对应方法中修改流程

---

### 2.3 业务模型层 (model.py)

**文件路径**: `model.py`

**功能职责**:
- 串口协议封装与解析
- 业务命令发送与响应处理
- 重试机制实现
- 数据缓冲管理

**核心类 SerialModel 的主要方法**:

| 方法 | 功能说明 | 涉及命令 |
|------|----------|----------|
| `get_software_version()` | 获取软件版本 | 0x0001 |
| `reset_device()` | 复位设备 | 0x0101 |
| `config_device()` | 配置设备参数 | 0x0002 |
| `read_device_config()` | 读取设备配置 | 0x0003 |
| `get_key_status()` | 获取密钥状态 | 0x0004 |
| `get_uid()` | 读取 UID | 0x0005 |
| `write_qi_key()` | 写入 Qi 密钥 | 0x0006 |
| `input_flash_driver()` | 下载 FlashDriver | 0x0201/0x0202/0x0203 |
| `send_flash_driver_start()` | 触发 FlashDriver 传输 | 0x0007 |

**发送重试机制**:
- 最大重试次数：3次
- 超时时间：1秒（普通命令）/ 30秒（OTA命令）
- 重试触发条件：
  1. 通讯超时
  2. data_type 不是 RESPONSE
  3. command 与请求不匹配

**修改指引**:
- 添加新命令：在 `data_processor.py` 的 `ValidValues` 中添加命令定义
- 修改协议格式：在 `SerialMessage` 类中修改解析逻辑
- 添加新业务：在 `SerialModel` 中添加新方法

---

### 2.4 数据处理模块 (utils/data_processor.py)

**文件路径**: `utils/data_processor.py`

**功能职责**:
- 串口消息协议定义与解析
- 配置参数结构定义
- 消息格式转换

#### 串口消息格式
```
┌────────┬────────────┬────────┬───────────┬─────────┬──────┬──────────┐
│ Header │ Data_Type  │ CMD    │ Data_Len  │  Data   │ CRC  │ End_Sym  │
│ 3 Byte │  1 Byte    │ 2 Byte │  2 Byte   │ N Byte  │1Byte │  2 Byte  │
├────────┴────────────┴────────┴───────────┼─────────┴──────┴──────────┤
│                                          │                              │
│              总长度 = 3 + 1 + 2 + 2 + N + 1 + 2 = 11 + N             │
└──────────────────────────────────────────┘
```

| 字段 | 长度 | 说明 |
|------|------|------|
| Header | 3 | 固定 "Lux" (0x4C 0x75 0x78) |
| Data_Type | 1 | 0x00=请求, 0x01=应答 |
| CMD | 2 | 命令码 |
| Data_Len | 2 | 数据长度（小端序） |
| Data | N | 业务数据体 |
| CRC | 1 | 数据体 CRC 校验 |
| End_Sym | 2 | 结束符 0x0D 0x0A |

#### 有效命令码

**普通命令（0x00xx）**:
| 命令码 | 名称 | 功能 |
|--------|------|------|
| 0x0001 | READ_SW_VERSION | 读软件版本号 |
| 0x0002 | CONFIG_PARAMS | 参数配置 |
| 0x0003 | READ_PARAMS | 参数读取 |
| 0x0004 | GET_KEY_STATUS | 获取密钥状态 |
| 0x0005 | READ_UID | 读UID |
| 0x0006 | WRITE_QI_KEY | 写Qi密钥 |
| 0x0007 | SEND_FLASH_DRIVER | 通知传输FlashDriver |

**复位命令（0x01xx）**:
| 命令码 | 名称 | 功能 |
|--------|------|------|
| 0x0101 | RESET | 复位设备 |

**FlashDriver OTA 命令（0x02xx）**:
| 命令码 | 名称 | 功能 |
|--------|------|------|
| 0x0201 | FLASH_START | 启动传输 |
| 0x0202 | FLASH_DATA | 数据传输 |
| 0x0203 | FLASH_END | 结束与总校验 |

#### 配置参数结构 (ConfigParams)

**TOML 配置文件格式**:
```toml
[CAN_config]
type = "CANFD"           # 通信类型: CAN/CANFD/LIN/Uart
baudrate = 2000          # 波特率
request_id = 0x724       # 诊断请求ID
response_id = 0x72C      # 诊断响应ID

[diag_did]
get_key_status = 0x4209  # 获取密钥状态DID
read_write_key = 0x420A  # 读写密钥DID

[Qi_certificate]
qi_transmit_id = 0x7F0   # Qi透传发送ID
qi_receive_id = 0x7F1    # Qi透传接收ID
get_qi_status = 0x420D   # 获取Qi状态DID

[nm_config]
nm_enabled = false       # 网络管理使能
nm_DLC = 15              # DLC (8=8字节, 15=64字节)
nm_id = 0x505            # 网络管理ID
nm_period = 200          # 周期(ms)
nm_message = "..."       # 报文内容

[FlashDriver]
FlashDriver_name = "xxx.bin"  # FlashDriver文件名
```

**修改指引**:
- 添加新命令：在 `ValidValues.COMMANDS` 添加新命令
- 修改配置结构：在 `ConfigParams` 中修改字段偏移量
- 修改协议格式：修改 `SerialMessage` 类的解析逻辑

---

### 2.5 串口通信模块 (utils/serial_handle.py)

**文件路径**: `utils/serial_handle.py`

**功能职责**:
- 封装 pyserial 库
- 提供跨平台的串口操作接口
- 串口异常自动重连

**核心类 SerialOperator**:

| 方法 | 功能说明 |
|------|----------|
| `list_available_ports()` | 获取可用串口列表 |
| `open_serial_port()` | 打开串口 |
| `close_serial_port()` | 关闭串口 |
| `send_data()` | 发送数据 |
| `receive_data()` | 接收数据 |

**修改指引**:
- 修改默认波特率：在 `open_serial_port()` 修改 `baudrate` 默认值
- 添加串口参数：在 `open_serial_port()` 添加新参数

---

### 2.6 API 客户端模块 (utils/api_client.py)

**文件路径**: `utils/api_client.py`

**功能职责**:
- 与 Qi 密钥服务器通信
- 用户登录认证
- 获取加密密钥

**API 接口**:

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/auth/login` | POST | 用户登录，获取 Token |
| `/api/encryption/encrypt` | POST | 根据 UID 获取加密密钥 |

**配置地址**: `config/api_config.py`

```python
API_BASE_URL = 'http://10.53.206.208:5000'
```

**修改指引**:
- 修改服务器地址：编辑 `config/api_config.py`
- 添加新接口：在 `ApiClient` 类添加新方法

---

### 2.7 FlashDriver 模块 (utils/flash_driver.py)

**文件路径**: `utils/flash_driver.py`

**功能职责**:
- FlashDriver 文件读取
- CRC32 计算
- 分片处理
- 配置文件解析

**关键函数**:

| 函数 | 功能说明 |
|------|----------|
| `get_file_path_from_config()` | 从配置获取 FlashDriver 路径 |
| `read_flash_driver_file()` | 读取 bin 文件 |
| `calculate_flash_driver_crc32()` | 计算 CRC32 |
| `get_flash_driver_chunk()` | 获取分片数据 |
| `chunk_flash_driver_data()` | 数据分片 |

**文件存储位置**: `output/FlashDriver/`

**修改指引**:
- 修改 FlashDriver 目录：修改 `_resolve_path()` 函数中的 `section` 值
- 修改分片大小：在 `data_processor.py` 修改 `MAX_APP_DATA_LENGTH`

---

### 2.8 视图层

#### 主窗口 (view/view.py)

**文件路径**: `view/view.py`

**功能职责**:
- 主界面 UI 管理
- 数据显示与日志输出
- 配置路径管理
- 状态栏管理

**核心类**:

| 类 | 功能说明 |
|----|----------|
| `MyComboBox` | 自定义下拉框，自动刷新串口列表 |
| `MyTextEdit` | 自定义文本框，支持大日志缓冲 |
| `View` | 主窗口类 |

**自定义组件说明**:

**MyComboBox**:
- 每次弹出时自动刷新可用串口列表
- 显示格式：`COMx # 串口描述`

**MyTextEdit**:
- 内存缓冲区最多 1000 条日志
- 超出部分写入临时文件
- 临时文件最多 50 个，每个最大 10MB
- 支持 Ctrl+S 保存日志

**修改指引**:
- 添加新按钮：在 `init_UI()` 中连接信号
- 修改界面布局：编辑 `panel/basic_main_window.ui`

#### 配置编辑窗口 (view/config_edit.py)

**文件路径**: `view/config_edit.py`

**功能职责**:
- 配置文件编辑
- 表格形式编辑网络管理报文
- 配置文件导入/导出

**核心类 ConfigEditWindow**:

| 功能区域 | 控件 | 说明 |
|----------|------|------|
| CAN配置 | typeComboBox | 通信类型选择 |
| CAN配置 | baudrateComboBox | 波特率选择 |
| CAN配置 | requestIDlineEdit | 请求ID |
| CAN配置 | responseIDlineEdit | 响应ID |
| 诊断DID | getKeyStatusDIDlineEdit | 密钥状态DID |
| 诊断DID | readWriteKeyDIDlineEdit | 读写密钥DID |
| Qi证书 | qiTransmitIDlineEdit | Qi发送ID |
| Qi证书 | qiReceiveIDlineEdit | Qi接收ID |
| Qi证书 | getQiStatusDIDlineEdit | Qi状态DID |
| 网络管理 | nmEnabledCheckBox | 使能开关 |
| 网络管理 | NMDLCcomboBox | DLC选择 |
| 网络管理 | NMIDlineEdit | 网络管理ID |
| 网络管理 | NMPeriodLineEdit | 周期设置 |
| 网络管理 | NMDataTableWidget | 报文编辑表格 |
| FlashDriver | FlashDriverNameLineEdit | 文件名 |

**快捷键**:
- `Ctrl+S` - 保存配置

**修改指引**:
- 添加新配置项：
  1. 在 `data_processor.py` 的 `ValidValues` 添加常量
  2. 在 `config_edit.py` 的 `Ui_configEditWindow` 添加控件
  3. 在 `_fill_ui_with_config()` 添加填充逻辑
  4. 在 `_get_config_from_ui()` 添加获取逻辑
  5. 在 `_save_config_to_file()` 添加保存格式

#### 登录对话框 (view/login_dialog.py)

**文件路径**: `view/login_dialog.py`

**功能职责**:
- 用户登录界面
- Token 管理

---

## 三、业务流程详解

### 3.1 串口连接流程
```
用户点击"连接"
       │
       ▼
Controller.toggle_serial()
       │
       ▼
创建 SerialCommunicationThread
       │
       ▼
Thread.run() → SerialModel.open_serial_port()
       │
       ▼
发射 result_signal
       │
       ▼
Controller.handle_serial_open_result()
       │
       ├─── 成功 ──► 启用操作按钮，获取软件版本
       │
       └─── 失败 ──► 显示错误，保持按钮状态
```

### 3.2 一键配置流程
```
用户点击"一键配置"
       │
       ▼
Controller.one_key_config()
       │
       ▼
SerialCommunicationThread.set_config_device()
       │
       ├─── 复位设备
       │
       ▼
       │
       ├─── 配置设备（发送 0x0002 命令）
       │
       ▼
       │
       ├─── 读取配置确认（发送 0x0003 命令）
       │
       ▼
       │
       ▼
根据配置判断是否需要下载 FlashDriver
       │
       ├─── 需要 ──► input_flash_driver()
       │            │
       │            ├─── 发送 0x0201 启动传输
       │            │
       │            ├─── 分包发送数据（0x0202）
       │            │
       │            └─── 发送 0x0203 结束校验
       │
       └─── 不需要 ──► 结束
```

### 3.3 写入 Qi 密钥流程
```
用户点击"写入Qi密钥"
       │
       ▼
Controller.write_qi_key()
       │
       ▼
获取设备 UID（0x0005 命令）
       │
       ▼
调用 ApiClient.get_encryption_key(uid)
       │
       ├─── Token 过期 ──► 弹出登录框
       │
       ▼
       │
       发送密钥到设备（0x0006 命令）
       │
       ▼
       │
显示结果
```

### 3.4 FlashDriver OTA 流程
```
步骤1: 发送启动命令 (0x0201)
       发送: [长度] (2字节小端序)
       接收: [状态码]
         - 0x00: 成功
         - 0x01: 设备忙
         - 0x02: 空间不足

步骤2: 分包发送数据 (0x0202)
       发送: [偏移(2字节)] + [数据(最大128字节)]
       接收: [状态码] + [期望偏移(2字节)]
       
       支持重传: 若设备返回的偏移 < 当前偏移，则重传

步骤3: 结束与校验 (0x0203)
       发送: [CRC32] (4字节小端序)
       接收: [校验结果]
         - 0x00: 成功
         - 0x01: CRC32校验失败
         - 0x02: 总长度不匹配
```

---

## 四、文件调用关系图

```
main.py
  └── Controller
        │
        ├──► View (view/view.py)
        │      ├──► Ui_MainWindow (panel/basic_main_window_ui.py)
        │      ├──► ConfigEditWindow (view/config_edit.py)
        │      │      └──► Ui_configEditWindow (panel/config_edit_ui.py)
        │      ├──► LoginDialog (view/login_dialog.py)
        │      └──► ApiClient (utils/api_client.py)
        │
        ├──► SerialModel (model.py)
        │      ├──► SerialOperator (utils/serial_handle.py)
        │      ├──► SerialMessage (utils/data_processor.py)
        │      ├──► ConfigParams (utils/data_processor.py)
        │      ├──► ValidValues (utils/data_processor.py)
        │      └──► flash_driver (utils/flash_driver.py)
        │             └──► file_utils (utils/file_utils.py)
        │
        └──► SerialCommunicationThread
               └──► (同 SerialModel 的依赖)
```

---

## 五、配置文件说明

### 5.1 tool-config.toml

**路径**: `tool-config.toml`

**用途**: 存储设备配置参数

**完整示例**:
```toml
# 配置 CAN 通信相关参数
[CAN_config]
type = "CANFD"
baudrate = 2000
request_id = 0x724
response_id = 0x72C

# 配置诊断 DID 相关参数
[diag_did]
get_key_status = 0x4209
read_write_key = 0x420A

# 配置 Qi 证书相关参数
[Qi_certificate]
qi_transmit_id = 0x7F0
qi_receive_id = 0x7F1
get_qi_status = 0x420D

# 配置网络管理相关参数
[nm_config]
nm_enabled = false
nm_DLC = 15
nm_id = 0x505
nm_period = 200
nm_message = """
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 11 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
"""

# 配置 FlashDriver 相关参数
[FlashDriver]
FlashDriver_name = "SBL_SHA256_Ver.bin"
```

### 5.2 last_config.ini

**路径**: `last_config.ini`

**用途**: 保存用户上次使用的配置和状态

**格式**: JSON
```json
{
    "path": "tool-config.toml",
    "serial_port": "COM3",
    "qi_api_token": "xxx",
    "qi_api_username": "user1"
}
```

### 5.3 api_config.py

**路径**: `config/api_config.py`

**用途**: API 服务器配置

```python
API_BASE_URL = 'http://10.53.206.208:5000'
LOGIN_URL = 'http://10.53.206.208:5000/api/auth/login'
GET_KEY_URL = 'http://10.53.206.208:5000/api/encryption/encrypt'
REQUEST_TIMEOUT = 10
```

---

## 六、日志系统

### 6.1 日志目录结构
```
save_data/
└── app_YYYYMMDD_info.log    # 每日日志文件
```

### 6.2 日志保留策略
- 保留天数: 7天
- 自动删除过期日志

### 6.3 日志格式
```
mm-dd HH:MM:SS.mmm [LEVEL] [filename      :line] message
```

---

## 七、修改维护指南

### 7.1 添加新命令

**步骤1**: 在 `data_processor.py` 添加命令定义
```python
# ValidValues 类中
COMMANDS_NEW_COMMAND = b'\x00\x08'     # 新命令码
COMMANDS = [..., COMMANDS_NEW_COMMAND] # 添加到列表
```

**步骤2**: 在 `SerialModel` 添加方法
```python
def new_command(self, params):
    message = SerialMessage.generate_new_message(
        ValidValues.DATA_TYPE_REQUEST,
        ValidValues.COMMANDS_NEW_COMMAND,
        params
    )
    return self.send_request_with_retry(message)
```

**步骤3**: 在 `controller.py` 添加调用方法
```python
def new_command_action(self):
    if self.serial_thread and self.serial_thread.isRunning():
        self.serial_thread.new_command(params)
```

**步骤4**: 在 `view.py` 连接信号
```python
self.view.ui.newButton.clicked.connect(self.new_command_action)
```

### 7.2 修改配置参数结构

**若添加新配置项**:

1. 在 `data_processor.py` 添加偏移量和长度常量
2. 在 `ConfigParams` 添加提取方法
3. 在 `config_edit.py` 的 UI 添加控件
4. 在 `_fill_ui_with_config()` 添加填充逻辑
5. 在 `_get_config_from_ui()` 添加获取逻辑
6. 更新 TOML 文件的读写逻辑

### 7.3 修改串口协议

**协议头修改**:
```python
# data_processor.py - ValidValues 类
HEADER_LUX = b'\x4C\x75\x78'  # 修改为新头
```

**校验方式修改**:
```python
# data_processor.py - SerialMessage.from_serial_data()
# 修改 CRC 校验逻辑
```

### 7.4 添加 API 接口

1. 在 `config/api_config.py` 添加端点
2. 在 `api_client.py` 添加方法
3. 在 `controller.py` 或 `view.py` 调用

---

## 八、常见问题排查

### 8.1 串口打开失败
- 检查串口是否被其他程序占用
- 检查串口号是否正确
- 检查驱动是否安装

### 8.2 配置下发失败
- 检查配置文件格式是否正确
- 检查设备是否在线
- 查看日志确认具体错误

### 8.3 FlashDriver 下载失败
- 检查 FlashDriver 文件是否存在
- 检查 CRC32 计算是否正确
- 检查设备存储空间是否足够

### 8.4 Qi 密钥写入失败
- 检查 Token 是否过期
- 检查 UID 是否正确
- 检查网络连接

---

## 九、联系方式

如有问题，请联系开发团队。

---

*本文档最后更新于 2026-07-06*