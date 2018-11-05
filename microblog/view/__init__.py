#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '02/08/2018'
"""
# import json

import sys
from flask import Flask, request, current_app, g
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.contrib.fixers import ProxyFix
from itsdangerous import URLSafeSerializer
from config import Config

#用户侧
from .m.member import bpm_member
from .m.blog import bpm_blog
from .m.comment import bpm_comment

def get_wsgi_app():

    # 定义了静态目录资源, 以及静态资源的访问context
    app = Flask(__name__, static_url_path='', static_folder='static')

    # Werkzeug 的 ProxyFix 来修复代理请求的问题
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # config
    app.config.from_object(Config)

    blueprints = (
        # 用户侧
        bpm_member, bpm_blog, bpm_comment,
      )

    for bp in blueprints:
        app.register_blueprint(bp)

    # DB
    app.sa_engine = engine_from_config(app.config["DB_OPTIONS"], prefix="")
    app.DBSession = scoped_session(sessionmaker(bind=app.sa_engine))

    app.signer = URLSafeSerializer(app.config["SECRET_KEY"])

    # 解决print或者文件读入写出时UnicodeEncodeError问题
    reload(sys)
    sys.setdefaultencoding('utf-8')

    @app.before_request
    def _before_request():

        #将传入的json信息转为dict并转为全局变量
        g.params = request.get_json()

        if request.endpoint == "static":
            return
        g.db = current_app.DBSession()
        if current_app.config.get('SESSION_ROLLBACK'):
            g.db.begin_nested()

    # @app.after_request
    # def _after_request(response):
    #     return response

    # @app.teardown_request
    # def _teardown_request(exception):
    #     if request.endpoint == "static":
    #         return
    #     if current_app.config.get('SESSION_ROLLBACK'):
    #         g.db.rollback()
    #     current_app.DBSession.remove()

    return app

# def write_log(response):
#     """ 记录操作日志
#     :param response:
#     :return:
#     """
#     # 是否正确返回
#     if '200' not in response.status:
#         return
#
#     try:
#         method = request.method.lower()
#         # 返回数据
#         res_data = json.loads(response.data) if response.data else {}
#
#         # 请求数据
#         if method == 'post' and 'application/json' in request.mimetype:
#             req_data = request.get_json() if request.data else {}
#         else:
#             req_data = dict((key, request.values.get(key)) for key in request.values.keys())
#
#         # 操作人信息
#         opt_member = {k: g.login_info.get(k) for k in ('id', 'phone')} if hasattr(g, 'login_info') else {}
#
#         log = {
#             'method': method,
#             'ip': request.remote_addr,
#             'p': opt_member,
#             'req_data': req_data,
#             'res_data': res_data if method == 'post' else {},
#             'path': request.path,
#             'datetime': '{}'.format(datetime.datetime.now())
#         }
#         current_app.opt_logger.info(json.dumps(log))
#     except:
#         pass
