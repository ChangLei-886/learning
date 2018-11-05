#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '08/02/2018'
"""
from flask import Blueprint, g
from model.comment import Comment
from model.member import Member
from model.base import get_model_by_field, model_query_by_field
from util.common import json_response
import collections
import copy

bpm_comment = Blueprint("mb_comment", __name__, url_prefix="/m")

#新评论登录
@bpm_comment.route('/comment/upload', methods=['POST'])
def do_comment_upload():
    # 新的评论信息插入
    # 将密码加密
    try:
        message = ''
        status = 0

        insert_dict = g.params

        login_name = insert_dict['login_name']
        #判断用户账号是邮件或者手机号
        if '@' in login_name:
            insert_dict['comment_email'] = login_name
        else:
            insert_dict['comment_phone'] = login_name

        insert_dict.pop('login_name')

        g.db.add(Comment(**insert_dict))

        g.db.commit()

    except Exception, e:
        message = repr(e)
        status = 1
        g.db.rollback()

    finally:
        return json_response(request=g.params, message=message, status=status)

#评论查询
@bpm_comment.route('/comment/query', methods=['POST'])
def do_comment_query():
    try:
        message = ''
        status = 0

        insert_dict = g.params
        # 博客ID
        blog_id = insert_dict['blog_id']
        # 起始页码
        page_index = insert_dict['page_index']
        # 一页显示行数
        page_size = insert_dict['page_size']

        records = model_query_by_field(model=Comment,
                                       page_index=page_index,
                                       page_size=page_size,
                                       field_name='blog_id',
                                       field_value=blog_id,
                                       sort_col=Comment.id,
                                       sort_desc=True)

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
        # 评论id
        ret_record['id'] = record.__dict__['id']
        # 博客ID
        ret_record['blog_id'] = record.__dict__['blog_id']
        # 评论内容
        ret_record['comment_text'] = record.__dict__['comment_text']
        # 发起人
        if record.__dict__['comment_phone'] is not None:
            recs = get_model_by_field(model=Member, field_name='phone', filed_value=record.__dict__['comment_phone'])

            if len(recs) > 0:
                ret_record['nickname'] = recs[0].__dict__['nickname']

        if record.__dict__['comment_email'] is not None:
            recs = get_model_by_field(model=Member, field_name='email', filed_value=record.__dict__['comment_email'])
            if len(recs) > 0:
                ret_record['nickname'] = recs[0].__dict__['nickname']

        # 创建日期
        ret_record['create_date'] = record.__dict__['create_time'].strftime("%Y-%m-%d")
        # 创建时间
        ret_record['create_time'] = record.__dict__['create_time'].strftime("%Y-%m-%d %H:%M:%S")

        ret_records.append(copy.deepcopy(ret_record))

    return ret_records