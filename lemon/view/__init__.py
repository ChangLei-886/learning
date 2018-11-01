#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '18/04/2017'
"""
import tornado.web

class Route(object):
    """ 把每个URL与Handler的关系保存到一个元组中，然后追加到列表内，列表内包含了所有的Handler """

    def __init__(self):
        self.urls = list()  # 路由列表

    def __call__(self, url, name=None):
        def register(cls):
            # 把路由的对应关系表添加到路由列表中
            self.urls.append(tornado.web.url(url, cls, name=name))
            return cls

        return register

route = Route()  # 创建路由表对象