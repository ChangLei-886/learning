#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by murphy.cong on '02/03/2018'
"""

class Config(object):
    SECRET_KEY = 'you-will-never-guess'

    # host define
    VOLGA_HOST = 'https://m.dev.xone.xin/volga'  # 用户侧
    DANUBE_HOST = 'https://man.dev.xone.xin/danube'  # 管理侧

    # 本地数据库
    DB_OPTIONS = {
        'url': 'mysql://root:!QAZ2wsx@127.0.0.1:3306/microblog?charset=utf8mb4',
        'pool_recycle': 3600,
        'echo': True
    }

class DevConfig(Config):
    # 是否开启debug模式, 默认False
    DEBUG = True


class TestConfig(Config):
    # 是否开启事务回归模式, 默认False
    SESSION_ROLLBACK = True


class ProductionConfig(Config):
    pass
