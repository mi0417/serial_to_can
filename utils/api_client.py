'''
API 客户端模块
用于与 Qi 密钥服务器的通信
'''
import logging
import requests
from typing import Optional, Tuple
import json

from config.api_config import LOGIN_URL, GET_KEY_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class ApiClient:
    '''API 客户端类，用于处理与 Qi 密钥服务器的通信'''

    def __init__(self):
        self._session = requests.Session()
        self._token: Optional[str] = None
        self._username: Optional[str] = None

    @property
    def token(self) -> Optional[str]:
        '''获取当前 token'''
        return self._token

    @property
    def username(self) -> Optional[str]:
        '''获取当前用户名'''
        return self._username

    def set_auth(self, token: str, username: str):
        '''设置认证信息'''
        self._token = token
        self._username = username
        logger.info('认证信息已保存到内存')

    def clear_auth(self):
        '''清除认证信息'''
        self._token = None
        self._username = None
        logger.info('认证信息已清除')

    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[str]]:
        '''
        登录获取 Token

        Args:
            username: 用户名
            password: 密码

        Returns:
            Tuple[bool, str, Optional[str]]:
            - success: 是否成功
            - message: 结果消息（成功或错误原因）
            - token: 成功时返回的 token，失败时为 None
        '''
        try:
            logger.info(f'开始登录，用户名: {username}')
            response = self._session.post(
                LOGIN_URL,
                json={'username': username, 'password': password},
                timeout=REQUEST_TIMEOUT
            )

            logger.debug(f'登录请求 URL: {LOGIN_URL}')
            logger.debug(f'登录请求数据: {{"username": "{username}", "password": "******"}}')
            logger.debug(f'登录响应状态码: {response.status_code}')
            logger.debug(f'登录响应内容: {response.text}')
            
            resp_data = response.json()
            if response.status_code == 200 and resp_data.get("token"):
                token = resp_data.get("token", "")
                if token:
                    self.set_auth(token, username)
                    logger.info('登录成功')
                    return True, '登录成功', token
                else:
                    logger.error('登录响应中未找到 token')
                    return False, '登录响应中未找到 token', None
            else:
                error_msg = resp_data.get("message", f"请求失败，状态码: {response.status_code}")
                logger.error(f'登录请求失败: {error_msg}')
                return False, error_msg, None

        except requests.exceptions.Timeout:
            logger.error('登录请求超时')
            return False, '请求超时，请检查网络连接', None
        except requests.exceptions.ConnectionError:
            logger.error('无法连接到服务器')
            return False, '无法连接到服务器，请检查网络', None
        except requests.exceptions.RequestException as e:
            logger.error(f'登录请求异常: {e}')
            return False, f'请求异常: {str(e)}', None
        except Exception as e:
            logger.error(f'登录时发生未知错误: {e}')
            return False, f'未知错误: {str(e)}', None

    def get_encryption_key(self, uid: str, token: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        '''
        获取加密密钥

        Args:
            uid: 设备 UID
            token: 可选的 token，如果为 None 则从 QSettings 获取

        Returns:
            Tuple[bool, str, Optional[str]]:
            - success: 是否成功
            - message: 结果消息
            - key: 成功时返回的密钥，失败时为 None
        '''
        if not token:
            token = self._token

        if not token:
            logger.warning('未找到 token，需要登录')
            return False, '401', None  # 需要登录

        try:
            logger.info(f'开始获取密钥，UID: {uid}')
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            response = self._session.post(
                GET_KEY_URL,
                json={'text': uid},
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

            logger.debug(f'获取密钥请求 URL: {GET_KEY_URL}')
            logger.debug(f'获取密钥请求参数: {{"text": "{uid}"}}')
            logger.debug(f'获取密钥请求头: {headers}')
            logger.debug(f'获取密钥响应状态码: {response.status_code}')
            logger.debug(f'获取密钥响应内容: {response.text}')
            if response.status_code == 200:
                data = response.json()
                key = data.get('encrypted')
                if key:
                    logger.info('获取密钥成功')
                    return True, '获取密钥成功', key
                else:
                    logger.error('密钥响应中未找到 key')
                    return False, '密钥响应中未找到 key', None
            elif response.status_code == 401:
                logger.warning('Token 过期，需要重新登录')
                self.clear_auth()
                return False, '401', None  # 需要重新登录
            elif response.status_code == 403:
                logger.error('无配额')
                return False, '403', None  # 无配额
            else:
                logger.error(f'获取密钥请求失败，状态码: {response.status_code}')
                return False, f'请求失败，状态码: {response.status_code}', None

        except requests.exceptions.Timeout:
            logger.error('获取密钥请求超时')
            return False, '请求超时，请检查网络连接', None
        except requests.exceptions.ConnectionError:
            logger.error('无法连接到服务器')
            return False, '无法连接到服务器，请检查网络', None
        except requests.exceptions.RequestException as e:
            logger.error(f'获取密钥请求异常: {e}')
            return False, f'请求异常: {str(e)}', None
        except Exception as e:
            logger.error(f'获取密钥时发生未知错误: {e}')
            return False, f'未知错误: {str(e)}', None

    def has_valid_token(self) -> bool:
        '''检查是否有有效的 token'''
        return self._token is not None and self._token != ''