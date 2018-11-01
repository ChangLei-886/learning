#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by murphy.cong on '07/08/2018'
"""

class Config(object):

    HOST = '127.0.0.1'
    PORT = 9000
    DEBUG = True
    TITLE = 'FPage'
    VERSION = '1.2.0'
    TEMPLATE = 'mako'  # jinja2/mako/tornado
    DATABASE_URI = "sqlite:///database.db"
    COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

    WECHAT_OPTIONS = {
        'appid': 'xx',
        'appsecret': 'xx',
    }

    # 验证用户第三方接口url
    VALIDATE_USER_URL = 'http://127.0.0.1:5000/m/validate_user/by_token'