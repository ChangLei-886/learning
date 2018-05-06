#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    # 用户名
    user_code = StringField('user_code', validators=[DataRequired()])
    # 用户密码
    password = StringField('password', alidators=[DataRequired()])

    # remember_me = BooleanField('remember_me', default=False)
