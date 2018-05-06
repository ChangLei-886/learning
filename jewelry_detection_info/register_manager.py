#!/usr/bin/env python
# encoding: utf-8

from model.crawler import User, DBSession

class RegisterManager:

    def __init__(self, user_code=None, user_name=None,
                       user_password=None,
                       confirm_password=None):
        self.session = DBSession()
        self.user_code = user_code
        self.user_name = user_name
        self.user_password = user_password
        self.confirm_password = confirm_password

    # 判断用户名是否存在
    def user_exists(self):

        if self.user_code is None:
            return False

        records = self.session.query(User).filter(User.user_code == self.user_code).all()

        if len(records) == 0:
            return False

        return True

    # 判断输入密码前后密码输入是否一致
    def password_check(self):
        return self.user_password == self.confirm_password

    # 插入用户注册记录
    def user_add(self):

        record = {'user_code': self.user_code,
                  'user_name': self.user_name,
                  'password': self.user_password}

        self.session.add(User(**record))

        self.session.commit()

    # 关闭session
    def session_close(self):

        self.session.close()
