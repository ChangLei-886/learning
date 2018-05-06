#!/usr/bin/env python
# encoding: utf-8

from model.crawler import User, DBSession

class LoginManager:

    def __init__(self, user_code=None, password=None):
        self.session = DBSession()
        self.user_code = user_code
        self.password = password

    # 判断用户名是否存在
    def user_exists(self):

        if self.user_code is None:
            return False

        records = self.session.query(User).filter(User.user_code == self.user_code).all()

        if len(records) == 0:
            return False

        return True

    # 判断登录密码是否正确
    def password_check(self):

        if self.user_code is None or self.password is None:
            return False

        records = self.session.query(User).filter(User.user_code == self.user_code,
                                                  User.password == self.password).all()

        if len(records) == 0:
            return False

        return True

    # 关闭session
    def session_close(self):

        self.session.close()
