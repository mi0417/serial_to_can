# SerialToCAN 项目结构分析

## 项目概述

密钥下载工具配置 —— 一个基于 PySide6 的串口转 CAN 工具上位机软件。

## 架构模式

**MVC 模式 (Model-View-Controller)**

```
main.py (入口)
    │
    ├─────────────┬───────────────┐
    ▼             ▼               ▼
Controller    Model          View
```

## 目录结构

```
SerialToCAN/
│
├── main.py                    # 程序入口，初始化应用和控制器
├── controller.py              # 业务逻辑控制器，处理用户交互
├── model.py                   # 数据模型，串口通信核心逻辑
│
├── view/                      # 视图层
│   ├── view.py               # 主窗口视图 (核心)
│   └── config_edit.py        # 配置编辑窗口视图
│
├── panel/                     # UI 文件目录
│   ├── basic_main_window.ui          # Qt Designer 设计文件
│   ├── basic_main_window_ui.py       # 生成的代码 (会覆盖!)
│   ├── config_edit.ui                 # Qt Designer 设计文件
│   ├── config_edit_ui.py              # 生成的代码 (会覆盖!)
│   ├── *.qss                          # 样式表文件
│   └── imgs/                          # 图片资源
│
├── utils/                     # 工具函数
│   ├── serial_handle.py       # 串口操作封装
│   ├── data_processor.py      # 数据解析、协议处理
│   ├── common_data_utils.py   # 通用数据转换
│   ├── file_utils.py          # 文件读写、路径处理
│   └── logger.py              # 日志管理
│
├── build/                     # PyInstaller 构建输出
├── output/                    # 配置文件和历史版本
└── test/                      # 测试文件
```

## 核心文件说明

| 文件 | 功能 | 优先级 |
|------|------|--------|
| main.py | 程序入口，初始化 QApplication 和 Controller | ⭐⭐⭐ |
| controller.py | 业务逻辑，控制 UI 与 Model 交互 | ⭐⭐⭐ |
| model.py | 串口通信、数据解析、重试逻辑 | ⭐⭐⭐ |
| view/view.py | 主界面 UI 逻辑、自定义控件 | ⭐⭐⭐ |
| view/config_edit.py | 配置编辑窗口逻辑 | ⭐⭐⭐ |

## 废弃文件清单

以下文件不再使用，可考虑删除：

### Panel 目录中的废弃文件

| 文件 | 说明 |
|------|------|
| basic_main_window_ui2.py | 旧版本备份，已被 view.py 中的覆盖逻辑替代 |
| main_window.ui | 早期 UI 设计，已废弃 |
| main_window_ui.py | 早期生成的代码，已废弃 |
| main_window_ui2.py | 早期版本备份，已废弃 |
| my_QWidget.py | 自定义控件，已合并到 view.py |

### 清理建议

```bash
# 可安全删除的文件
panel/basic_main_window_ui2.py
panel/main_window.ui
panel/main_window_ui.py
panel/main_window_ui2.py
panel/my_QWidget.py
```

## UI 文件覆盖机制

Qt Designer 修改 .ui 文件后，用 pyside6-uic 重新生成代码时会导致自定义修改丢失。

### 解决方案

**旧方法** (文件多，难维护)：
```
修改 ui.py → 复制到 _ui2.py → 修改 _ui2.py
```
缺点：每次 UI 变更都需要手动合并

**当前方法** (推荐)：
```
不修改 *_ui.py，在 view.py 中动态替换控件
```

示例 (view.py)：
```python
# 替换原生控件为自定义控件
self.ui.serialBox = self.replace_combo_box(self.ui.serialBox, self)
self.ui.logEdit = self.replace_text_edit(self.ui.logEdit, self)
```

## 文件引用关系

```
main.py
  └─> from controller import Controller
        └─> from model import SerialModel
        └─> from view.view import View
              └─> from panel.basic_main_window_ui import Ui_MainWindow
              └─> from view.config_edit import ConfigEditWindow
                    └─> from panel.config_edit_ui import Ui_configEditWindow
```

## 快速导航

### 添加新功能的推荐位置

| 功能类型 | 推荐添加位置 |
|----------|-------------|
| 界面调整 | view/view.py |
| 业务逻辑 | controller.py |
| 串口通信 | model.py |
| 数据解析 | utils/data_processor.py |
| 新窗口 | view/ 新建 xxx.py |

### 避免修改的文件 (会被覆盖)

- panel/basic_main_window_ui.py
- panel/config_edit_ui.py

---

*生成时间: 2026-06-18*