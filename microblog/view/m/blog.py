#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '08/02/2018'
"""
from flask import Blueprint, g
from model.blog import Blog
from model.member import Member
from util.common import json_response
from model.base import get_model_by_field

from model.base import model_query
import collections
from datetime import datetime

bpm_blog = Blueprint("mb_blog", __name__, url_prefix="/m")



#新博客登录
@bpm_blog.route('/blog/upload', methods=['POST'])
def do_blog_upload():
    # 新的博客信息插入
    # 将密码加密
    try:
        message = ''
        status = 0

        insert_dict = g.params

        login_name = insert_dict['login_name']
        #判断用户账号是邮件或者手机号
        if '@' in login_name:
            insert_dict['sponsor_email'] = login_name
        else:
            insert_dict['sponsor_phone'] = login_name

        insert_dict.pop('login_name')

        g.db.add(Blog(**insert_dict))

        g.db.commit()

    except Exception, e:
        message = repr(e)
        status = 1
        g.db.rollback()

    finally:
        return json_response(request=g.params, message=message, status=status)

#博客主题查询
@bpm_blog.route('/blog/query', methods=['POST'])
def do_blog_query():

    try:
        message = ''
        status = 0

        insert_dict = g.params

        # 起始页码
        page_index = insert_dict['page_index']
        # 一页显示行数
        page_size = insert_dict['page_size']

        records = model_query(model=Blog, page_index=page_index, page_size=page_size, sort_col=Blog.id, sort_desc=True)

    except Exception, e:

        message = repr(e)
        status = 1
    finally:

        return json_response(request=g.params, response=model_query_clear(records), message=message, status=status)

# 对于model检索出来的all结果集进行再加工
def model_query_clear(records):

    ret_records = []
    ret_record = collections.OrderedDict()
    for record in records:
        # 博客id
        ret_record['id'] = record.__dict__['id']
        # 博客主题
        ret_record['blog_subject'] = record.__dict__['blog_subject']
        # 发起人
        if record.__dict__['sponsor_phone'] is not None:
            recs = get_model_by_field(model=Member, field_name='phone', filed_value=record.__dict__['sponsor_phone'])

            if len(recs) > 0:
                ret_record['nickname'] = recs[0].__dict__['nickname']

        if record.__dict__['sponsor_email'] is not None:
            recs = get_model_by_field(model=Member, field_name='email', filed_value=record.__dict__['sponsor_email'])
            if len(recs) > 0:
                ret_record['nickname'] = recs[0].__dict__['nickname']

        # 创建日期
        ret_record['create_date'] =  record.__dict__['create_time'].strftime("%Y-%m-%d")
        # 创建时间
        ret_record['create_time'] = record.__dict__['create_time'].strftime("%Y-%m-%d %H:%M:%S")

        ret_records.append(ret_record)

    return ret_records