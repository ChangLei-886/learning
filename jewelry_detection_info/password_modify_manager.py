#!/usr/bin/env python
# encoding: utf-8

from model.crawler import User, DBSession
from datetime import datetime

class PasswordModifyManager:

    def __init__(self, user_code=None,
                       old_password=None,
                       new_password=None,
                       confirm_password=None):
        self.session = DBSession()
        self.user_code = user_code
        self.old_password = old_password
        self.new_password = new_password
        self.confirm_password = confirm_password

    # 判断用户名是否存在
    def user_exists(self):

        if self.user_code is None:
            return False

        records = self.session.query(User).filter(User.user_code == self.user_code).all()

        if len(records) == 0:
            return False

        return True
    # 判断原密码是否正确
    def old_password_check(self):

        records = self.session.query(User).filter(User.user_code == self.user_code).all()

        if len(records) == 0:
            return False

        record = records[0]
        if record.password != self.old_password:
            return False

        return True

    # 判断输入密码前后密码输入是否一致
    def new_password_check(self):
        return self.new_password == self.confirm_password

    # 插入用户注册记录
    def user_password_modify(self):

        record = {'password': self.new_password,
                  'update_time': datetime.now()}

        self.session.query(User).filter(User.user_code == self.user_code).update(record)

        self.session.commit()

    # 关闭session
    def session_close(self):

        self.session.close()
