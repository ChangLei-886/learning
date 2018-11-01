# encoding:utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by murphy.cong on 1/14/16
"""
import tornado.ioloop
from sys import argv

from view import route
from config import Config
from view import view


application = tornado.web.Application(
    route.urls,
    debug=Config.DEBUG,
    cookie_secret=Config.COOKIE_SECRET,
    xsrf_cookies=False,
)

if __name__ == "__main__":
    if len(argv) > 1 and argv[1][:6] == '-port=':
        Config.PORT = int(argv[1][6:])

    application.listen(Config.PORT, address=Config.HOST)
    print('Server started at %s:%s' % (Config.HOST, Config.PORT))
    tornado.ioloop.IOLoop.instance().start()

