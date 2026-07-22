'''
登录对话框模块
'''
import logging
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal, Qt

logger = logging.getLogger(__name__)


class LoginDialog(QDialog):
    '''登录对话框，用于输入用户名和密码'''

    login_successful = Signal(str)  # 登录成功信号，携带 token

    def __init__(self, api_client, default_username: str = None):
        super().__init__()
        self.api_client = api_client
        self.default_username = default_username
        self.token = None
        self._setup_ui()
        self._load_saved_username()

    def _setup_ui(self):
        '''设置 UI'''
        self.setWindowTitle('登录立讯 Qi 密钥服务')
        self.setModal(True)
        self.setMinimumWidth(350)

        # 主布局
        main_layout = QVBoxLayout(self)

        # 表单布局
        form_layout = QFormLayout()

        # 用户名输入
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        self.username_edit.returnPressed.connect(self._on_login_clicked)
        form_layout.addRow('用户名:', self.username_edit)

        # 密码输入
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.returnPressed.connect(self._on_login_clicked)
        form_layout.addRow('密码:', self.password_edit)

        main_layout.addLayout(form_layout)

        # 按钮布局
        button_layout = QHBoxLayout()

        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self._on_login_clicked)
        button_layout.addWidget(self.login_button)

        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

    def _load_saved_username(self):
        '''加载保存的用户名'''
        if self.default_username:
            self.username_edit.setText(self.default_username)
        else:
            saved_username = self.api_client.username
            if saved_username:
                self.username_edit.setText(saved_username)

    def _on_login_clicked(self):
        '''处理登录按钮点击'''
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        if not username:
            QMessageBox.warning(self, '输入错误', '请输入用户名')
            self.username_edit.setFocus()
            return

        if not password:
            QMessageBox.warning(self, '输入错误', '请输入密码')
            self.password_edit.setFocus()
            return

        self.login_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.login_button.setText('登录中...')

        try:
            success, message, token = self.api_client.login(username, password)

            if success:
                self.token = token
                logger.info(f'登录对话框登录成功，用户名: {username}')
                self.accept()
            else:
                QMessageBox.critical(self, '登录失败', message)
                self.login_button.setEnabled(True)
                self.cancel_button.setEnabled(True)
                self.login_button.setText('登录')
                self.password_edit.clear()
                self.password_edit.setFocus()
        except Exception as e:
            logger.error(f'登录过程异常: {e}')
            QMessageBox.critical(self, '错误', f'登录过程中发生错误: {str(e)}')
            self.login_button.setEnabled(True)
            self.cancel_button.setEnabled(True)
            self.login_button.setText('登录')

    def get_token(self) -> str:
        '''获取登录后的 token'''
        return self.token