#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '03/08/2018'
"""

from flask import g
from model.member import Member


# 通过列的值检索相对应的结果集
def get_model_by_field(model, field_name='', filed_value=''):
    """ 根据model的某个字段,查看第一个符合体检的model
    :param field_name:
    :param filed_value:
    :return:
    """
    return g.db.query(model).filter(getattr(model, field_name) == filed_value).first()


# 修改用户名密码
def user_password_modify(login_name='', password_crypt=''):

    record = {'password_crypt': password_crypt}

    if '@' not in login_name:
        g.db.query(Member).filter(Member.phone == login_name).update(record)
    else:
        g.db.query(Member).filter(Member.email == login_name).update(record)

    g.db.commit()


# 查询表的结果集
def model_query(model, page_index=1, page_size=10, sort_col=None, sort_desc=False):

    if not sort_col:
        # g.db.query().filter().group_by().limit().first().all().scalar()

        return g.db.query(model).filter().slice((page_index - 1) * page_size,
                                                                 page_index * page_size).all()
    else:
        if sort_desc:
            return g.db.query(model).filter().order_by(sort_col.desc()).slice((page_index - 1) * page_size,
                                                    page_index * page_size).all()
        else:
            return g.db.query(model).filter().order_by(sort_col).slice((page_index - 1) * page_size,
                                                                                    page_index * page_size).all()

# 查询表的结果集
def model_query_by_field(model, page_index=1, page_size=10,
                         field_name='', field_value='', sort_col=None, sort_desc=False):

    if not sort_col:
        return g.db.query(model).filter(getattr(model, field_name) == field_value).slice((page_index - 1)
                                                    * page_size, page_index * page_size).all()
    else:
        if sort_desc:
            return g.db.query(model).filter(getattr(model, field_name) == field_value).order_by(sort_col.desc()).slice((page_index - 1)
                                                    * page_size, page_index * page_size).all()
        else:
            return g.db.query(model).filter(getattr(model, field_name) == field_value).order_by(sort_col).slice((page_index - 1)
                                                    * page_size, page_index * page_size).all()








