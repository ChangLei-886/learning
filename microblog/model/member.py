#!/usr/bin/env python
# encoding: utf-8
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    created by murphy.cong on '06/03/2017'
"""
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class Member(Base):
    """ 用户信息
    """
    __tablename__ = "mb_member"
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    nickname = Column(VARCHAR(40), nullable=False, server_default='')
    realname = Column(VARCHAR(40), nullable=False, server_default='')
    password_crypt = Column(VARCHAR(200), nullable=False, server_default='')
    phone = Column(VARCHAR(20), unique=True)
    email = Column(VARCHAR(40), unique=True)
    create_time = Column(DATETIME, nullable=False, server_default=func.now())
    update_time = Column(TIMESTAMP, nullable=False)

    # GENDER_FEMALE, GENDER_MALE, GENDER_UNKNOWN = 0, 1, 2
    #
    # _columns_extra_modify = ['password']
    # _columns_no_display = ['password_crypt']

    # def set_password(self, raw_password):
    #     if raw_password is None:
    #         self.password_crypt = None
    #         return
    #     self.password_crypt = sha512_crypt.encrypt(raw_password, rounds=1000)
    #
    # # password联动encrypted_password
    # password = property(fset=set_password)

    # def verify_password(self, raw_password):
    #     """ 验证密码
    #     :param raw_password:
    #     :return:
    #     """
    #     if not self.password_crypt:
    #         return False
    #     return sha512_crypt.verify(raw_password, self.password_crypt)

    @classmethod
    def modify_password(cls, member_id, password_ori, password):
        """ 修改密码
        :param member_id:
        :param password_ori:
        :param password:
        :return:
        """
        member = Member.get_model(member_id)
        if not member.password_crypt:
            member.password = password
        elif member.verify_password(password_ori):
            member.password = password
        else:
            raise BizError(u'原密码输入错误')
        try:
            g.db.commit()
        except:
            g.db.rollback()
            raise

    @classmethod
    def reset_password(cls, member_id, password):
        """ 重置密码
        :param member_id:
        :param password:
        :return:
        """
        member = Member.get_model(member_id)
        member.password = password
        try:
            g.db.commit()
        except:
            g.db.rollback()
            raise
        return

    # @classmethod
    # def signup_with_oauth(cls, user_dict, opt):
    #     """ 第三方认证生成账号, 如果手机已存在, 则绑定原来的用户
    #     :param user_dict:
    #     :param opt:
    #     :return:
    #     """
    #     # 如果用户不存在, 则新建用户, 给用户赋值, avatar 取到本地
    #     try:
    #         avatar = QiniuUtil().fetch_remote_img(user_dict.get('avatar'), 'p/avatar')
    #     except:
    #         avatar = ''
    #     try:
    #         user_dict['avatar'] = avatar
    #
    #         member = Member()
    #         member.set_model_value(user_dict)
    #         g.db.add(member)
    #         g.db.commit()
    #     except:
    #         g.db.rollback()
    #         raise
    #     # 日志, 这里注意
    #     MemberLog.write_login_log(member.id, opt)
    #     return member
