#encoding: utf-8

# 从flask这个框架中导入Flask这个类
import os
from flask import Flask, render_template, request, json, redirect, url_for
# from mypackage.werkzeug2 import secure_filename
from werkzeug.utils import secure_filename
import config
# from gtwisted.core import reactor
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

# 初始化一个Flask对象
# Flask()
# 需要传递一个参数__name__
# 1.方便flask框架去寻找资源
# 2.方便flask插件Flask-Sqlalchemy出现错误的时候，好去寻找问题所在的位置

# print __name__
# app = Flask(__name__)
# app.config.from_object(config)
# MAX_PAGE = 10

#

# app.route是一个装饰器
# @开头，并且在函数的上面，说明是装饰器
# 这个装饰器的作用，是做一个url与视图函数的映射
# 127.0.0.1:5000/ -> 去请求hello_world这个函数，然后将结果返回给浏览器。
# @app.route('/index', methods=['GET', 'POST'])
# @app.route('/index?page=<page>', methods=['GET', 'POST'])
# def index(page=1):
#     context = {
#         'username': u"畅垒",
#         'gender': u"男",
#         'age': "33",
#         'current_page': page,
#         'max_page': MAX_PAGE
#     }
#
#     if request.method == 'POST':
#         if not request.form.get('page') or int(request.form.get('page')) < 1:
#             context['current_page'] = 1
#         else:
#             if int(request.form.get('page')) > MAX_PAGE:
#                 context['current_page'] = MAX_PAGE
#             else:
#                 context['current_page'] = request.form.get('page')
#
#     return render_template('index.html', **context)
#
#
# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         filename = secure_filename(f.filename)
#         print(filename)
#
#         # f.save('/Users/changlei/PycharmProjects/flask_project/static/%s' % (str(filename)))
#         return 'ok'
#     else:
#         return render_template('upload.html')
#
# from flask import make_response , send_file
#
# @app.route('/download', methods=['GET'])
# def download():
#
#     response = make_response(send_file("views.py"))
#
#     response.headers["Content-Disposition"] = "attachment; filename=views.py;"
#
#     return response
#
# def get_page_index():
#     return 10
#
# with app.test_request_context('/', method='POST'):
#     assert request.path
#     assert request.method
#
# # 如果当前这个文件是作为入口程序运行，那么就执行app.run()
# if __name__ == '__main__':
#     # app.run()
#     # 启动一个能用服务器，来接受用户的请求
#     # while True():
#     #   listen()
#     app.run()
app1 = Flask('app1')
app2 = Flask('app2')


@app1.route("/index1")
def index1():
    return "app1"


@app1.route("/home")
def home():
    return "app1home"


@app2.route("/index2")
def index2():
    return "app2"


# app = DispatcherMiddleware(app1, {'app2': app2})

app = DispatcherMiddleware(app1, {'/app2': app2, })

if __name__ == '__main__':
    run_simple('localhost', 5000, app)

# reactor.listenWSGI(8000, app1)
# reactor.listenWSGI(8001, app2)
# reactor.run()


# with app1.test_request_context():
#     print url_for('index1')
# with app2.test_request_context():
#     print url_for('index2')
    # print url_for('home')

