#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '08/02/2018'
"""
from flask import Blueprint, g
from model.member import Member
from util.common import get_md5, json_response
from model.base import get_model_by_field, user_password_modify

bpm_member = Blueprint("mb_member", __name__, url_prefix="/m")

#判断该用户是否存在
def check_member_exists(login_name=None):
    if not login_name:
        return False

    if '@' in login_name:
        records = get_model_by_field(model=Member, field_name='email', filed_value=login_name)
    else:
        records = get_model_by_field(model=Member, field_name='phone', filed_value=login_name)

    if len(records) == 0:
        return False

    return True

#新用户注册
@bpm_member.route('/sign/register', methods=['POST'])
def do_register():
    """
        :desc: 登陆
        :url: /m/sign/register
        :method: POST
        :param:

            - login_name:  用户名
            - password:  密码

        """

    # 将新用户的注册信息插入
    # 将密码加密
    try:
        message = ''
        status = 0

        insert_dict = g.params

        #判断该用户是否已经注册
        if check_member_exists(login_name=insert_dict['phone']) or \
           check_member_exists(login_name=insert_dict['email']):
            message = u'该用户已存在!'
            status = 1
            return
        #得到加密后密码
        insert_dict['password_crypt'] = get_md5(insert_dict['password'])
        #删除未加密密码值,才能插入到member表
        insert_dict.pop('password')

        g.db.add(Member(**insert_dict))

        g.db.commit()

    except Exception, e:
        message = repr(e)
        status = 1
        g.db.rollback()

    finally:
        return json_response(request=g.params, message=message, status=status)

@bpm_member.route('/sign/login', methods=['POST'])
def do_login():
    """
    :desc: 登陆
    :url: /m/login
    :method: POST
    :param:

        - login_name:  用户名
        - password:  密码
    """
    try:
        message = ''
        status = 0

        login_name = g.params.get('login_name')
        #用户名不存在
        if not check_member_exists(login_name):
            message = '用户名错误!'
            status = 1
            return

        records = []
        #判断密码是否正确
        if '@' in login_name:
            records = get_model_by_field(Member, 'email', login_name)
        else:
            records = get_model_by_field(Member, 'phone', login_name)

        # for record in records:
        password_crypt = records[0].__dict__['password_crypt']

        if password_crypt != get_md5(g.params.get('password')):
            message = '密码错误!'
            status = 1
            return

    except Exception, e:
        message = repr(e)
        status = 1
        g.db.rollback()
    finally:
        return json_response(request=g.params, message=message.encode(encoding='utf-8'), status=status)

    # # 设置登录session
    # login_info = set_login_manager_info(login_info)
    # return json_response(data=login_info)

# @bpm_member.route('/sign/login_by_token', methods=['POST'])
# def do_login_by_token():
#     """
#     :desc: 通过token登录
#     :url: /m/login_by_token
#     :method: POST
#     :param:
#
#         - access_token:  token
#
#     :return:
#     """
#     access_token = g.params.get('access_token')
#     login_info = get_login_manager_info(access_token=access_token)
#     return json_response(data=login_info)
#
#
# @bpm_member.route('/sign/is_login')
# def is_login():
#     """
#     :desc: 查询用户是否登录
#     :url: /m/is_login
#     :method: GET
#     :param:
#
#     :return:
#     """
#     return json_response(data=g.login_info)
#
#
# @bpm_member.route('/sign/logout', methods=['POST'])
# def do_logout():
#     """
#     :desc: 登出
#     :url: /m/logout
#     :method: POST
#     :param:
#
#     :return:
#     """
#     current_manager_logout()
#     return json_response()
#
#
@bpm_member.route('/profile/password_modify', methods=['POST'])
def modify_password():
    """
    :desc: 修改密码
    :url: /m/profile/password_modify
    :method: POST
    :param: json数据::

        - password_ori: 原密码
        - password: 密码

    :return:
    """
    try:
        message = ''
        status = 0

        insert_dict = g.params
        #用户名
        login_name = insert_dict['login_name']
        #密码
        password = insert_dict['password']
        # 判断该用户是否存在
        if not check_member_exists(login_name=login_name) and \
           not check_member_exists(login_name=login_name):
            message = u'该用户不存在!'
            status = 1
            return

        #修改用户登录密码
        user_password_modify(login_name=login_name, password_crypt=get_md5(password))


    except Exception, e:
        message = repr(e)
        status = 1
    finally:
        return json_response(request=g.params, message=message.encode(encoding='utf-8'), status=status)
