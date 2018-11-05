#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by lei.chang on '02/08/2018'
"""
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class Comment(Base):
    """ 博客评论信息
    """
    __tablename__ = "mb_comment"
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    blog_id = Column(INTEGER, nullable=False)
    comment_text = Column(VARCHAR(200), nullable=False, server_default='')
    comment_phone = Column(VARCHAR(20))
    comment_email = Column(VARCHAR(40))
    create_time = Column(DATETIME, nullable=False, server_default=func.now())
    update_time = Column(TIMESTAMP, nullable=False)
