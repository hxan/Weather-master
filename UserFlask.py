# author:l
# contact: test@test.com
# datetime:2022/6/13 17:06
# software: PyCharm
# file    : UserFlask.py
# description :

from flask_login import UserMixin  # 引入用户基类
from werkzeug.security import check_password_hash
import uuid

USERS = []

class User(UserMixin):
    """用户类"""

    def __init__(self, username, password, address):

        self.username = username
        self.password_hash = password
        self.id = uuid.uuid4()
        self.address = address

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        '''判断是否登录'''
        return True

    def is_active(self):
        '''同上'''
        return True

    def is_anonymous(self):
        '''是不是匿名'''
        return False

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None
