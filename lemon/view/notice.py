#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '01/11/2018'
"""
import json
from tornado import websocket, web
from view import route
from  config import Config
import requests
from requests.exceptions import RequestException
from core.constant import Constant


@route('/websocket/send')
class NoticeHandler(web.RequestHandler):
    """ 接受远程的http请求，接受服务器的消息发送
    """
    def get(self):
        self.finish('success')

    def post(self):

        data = json.loads(self.request.body)
        print(data)

        # 查看是哪个项目的websocket
        msg_cls = MsgWebSocket

        send_to = data.pop('send_to', None)

        # 商城消息
        if send_to == Constant.TO_MALL:
            socket_map = msg_cls.member_socket_map
        # 运营人员消息
        elif send_to == Constant.TO_MANAGER:
            socket_map = msg_cls.operator_socket_map
        else:
            self.finish('请求参数/格式错误')

        to_some_one = data.pop('to_some_one', None)

        if to_some_one:
            # 给某些人推送
            member_ids = to_some_one
            for member_id in member_ids:
                member_socket = socket_map.get(member_id)
                if member_socket:
                    member_socket.write_message(data)
        else:
            # 给全部人推送
            for member_id, socket in socket_map.items():
                socket.write_message(data)

        self.finish('success')

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')


@route('/websocket/register')
class MsgWebSocket(websocket.WebSocketHandler):
    """ 用户验证
    """
    member_socket_map = {}   # 商城用户
    operator_socket_map = {}  # 运营人员

    def check_origin(self, origin):
        return True

    def open(self):
        pass

    def on_message(self, message):
        data = json.loads(message)
        # 事件类型
        event = data.get('event')
        # 用户id
        member_id = data.get('member_id')
        # 运营人员
        operator_id = data.get('operator_id')
        # token
        token = data.get('token')
        # 参数检查
        user_id = member_id if member_id else operator_id
        if not event or not user_id or not token:
            self.write_message('请求参数/格式错误')

        # 用户校验
        if event == Constant.EVENT_REGISTER:
            params = {'user_id': user_id,
                      'token': token}

            url = Config.VALIDATE_USER_URL
            try:
                rsp = requests.get(url=url, params=params)
            except RequestException:
                self.write_message('用户验证失败')
            # 必须指定编码, 否则乱码
            rsp.encoding = 'utf-8'
            ret_data = rsp.json()
            result = ret_data['data']['result']

            # 验证成功
            if result:
                if member_id:
                    self.member_socket_map[member_id] = self
                if operator_id:
                    self.operator_socket_map[operator_id] = self

                self.write_message('用户验证成功')
            else:
                self.write_message('用户验证未通过')
        else:
            self.write_message('请求参数/格式错误')

    def on_close(self):
        for k, v in self.member_socket_map.items():
            if v == self:
                self.member_socket_map.pop(k, None)

