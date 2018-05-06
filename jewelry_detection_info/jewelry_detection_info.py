#encoding:utf-8
import sys
import copy
import collections
from flask import Flask, render_template, url_for, redirect, request, flash, session as se
from model.crawler import DectectionInfo, FieldsInfoMapper, DBSession
from login_manager import LoginManager
from register_manager import RegisterManager
from password_modify_manager import PasswordModifyManager as PMM
from config import Config

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

config = Config()

app.secret_key = config.SECRET_KEY

app.config['PERMANENT_SESSION_LIFETIME'] = Config.PERMANENT_SESSION_LIFETIME

#
def data_from_crawler(tablename='detection_information'):

    # 创建session对象
    session = DBSession()

    if tablename == 'detection_information':
        dectectionInfos = session.query(DectectionInfo).all()
    elif tablename == 'fields_mapper_info':
        dectectionInfos = session.query(FieldsInfoMapper).all()

    records = []
    record = {}
    for dectectionInfo in dectectionInfos:
        #
        record.update(dectectionInfo.__dict__)

        record.pop('_sa_instance_state')

        records.append(copy.deepcopy(record))

    # 关闭session:
    session.close()

    return records

def data_from_detection_info(detection_number=None,query_code=None):

    # 创建session对象
    session = DBSession()

    dectectioninfo = session.query(DectectionInfo).filter(DectectionInfo.detection_number==detection_number,
                                                            DectectionInfo.query_code==query_code).one()


    # 得到显示项目列表
    fields_mapper_infos = session.query(FieldsInfoMapper).filter(FieldsInfoMapper.source_url ==
                                                                 dectectioninfo.source_url).all()

    record = collections.OrderedDict()

    for fields_mapper_info in fields_mapper_infos:

        record[fields_mapper_info.disply_name] = dectectioninfo.__dict__[fields_mapper_info.field_name]

    print record
    return record

    # 关闭session:
    session.close()

@app.route('/query')
def detection_info_show():

    # 得到检测项目信息表
    records = data_from_crawler('detection_information')

    for record in records:
        print record

    datas = {'records': records, 'detection_number': '', 'query_code': ''}
    return render_template('index.html', **datas)

# 详情页面
@app.route('/details/<detection_number>/<query_code>')
def detection_details_show(detection_number=None, query_code=None):

    record = data_from_detection_info(detection_number, query_code)

    datas = {'record': record, 'detection_number': detection_number, 'query_code': query_code}

    return render_template('details.html', **datas)

# 登录页面
@app.route('/')
def init():
    return redirect(url_for('login', user_code=' '))

@app.route('/login/<user_code>')
def login(user_code=' '):
    datas = {'user_code': user_code}
    return render_template('login.html', **datas)

@app.route('/login/<user_code>', methods=['POST'])
def do_login(user_code=' '):
    # 用户名
    user_code = request.form.get('user_code')
    # 密码
    password = request.form.get('password')

    login_manager = LoginManager(user_code, password)

    if not login_manager.user_exists():
        flash("Error: 用户名不存在！")
        # 关闭session
        login_manager.session_close()
        return redirect(url_for('login', user_code=user_code))
    if not login_manager.password_check():
        flash("Error: 密码错误！")
        # 关闭session
        login_manager.session_close()
        return redirect(url_for('login', user_code=user_code))

    # 关闭session
    login_manager.session_close()

    return redirect(url_for('detection_info_show'))

# 注册页面
@app.route('/register/<user_code>/<user_name>')
def register(user_code=' ', user_name=' '):

    return render_template('register.html', user_code=user_code, user_name=user_name)

@app.route('/register/<user_code>/<user_name>', methods=['POST'])
def do_register(user_code=' ', user_name=' '):
    # 用户名
    user_code = request.form.get('user_code')
    # 用户名称
    user_name = request.form.get('user_name')
    # 用户密码
    password = request.form.get('password')
    # 确认密码
    confirm_password = request.form.get('confirm_password')

    register_manager = RegisterManager(user_code=user_code,
                                       user_name=user_name,
                                       user_password=password,
                                       confirm_password=confirm_password)

    if register_manager.user_exists():
        flash('Error: 用户名已经存在!')
        register_manager.session_close()
        return redirect(url_for('register', user_code=user_code, user_name=user_name))

    if not register_manager.password_check():
        flash('Error: 前后密码不一致!')
        register_manager.session_close()
        return redirect(url_for('register', user_code=user_code, user_name=user_name))

    # 插入该条注册信息
    register_manager.user_add()

    flash('Success: 用户注册成功!')
    # 返回登录页面
    return redirect(url_for('login', user_code=user_code))

# 修改密码页面
@app.route('/password_modify/<user_code>/<old_password>/<new_password>/<confirm_password>')
def change_password(user_code=' ',
                    old_password=' ',
                    new_password=' ',
                    confirm_password=' '):

    return render_template('password_modify.html', user_code=user_code,
                                                   old_password=old_password,
                                                   new_password=new_password,
                                                   confirm_password=confirm_password)

@app.route('/password_modify/<user_code>/<old_password>/<new_password>/<confirm_password>', methods=['POST'])
def do_change_password(user_code=' ',
                       old_password=' ',
                       new_password=' ',
                       confirm_password=' '):
    # 用户名
    user_code = request.form.get('user_code')
    # 原密码
    old_password = request.form.get('old_password')
    # 新密码
    new_password = request.form.get('new_password')
    # 确认密码
    confirm_password = request.form.get('confirm_password')

    pmm = PMM(user_code=user_code,
              old_password=old_password,
              new_password=new_password,
              confirm_password=confirm_password)

    if not pmm.user_exists():
        flash('Error: 用户名不存在!')
        pmm.session_close()
        return redirect(url_for('change_password', user_code=user_code,
                                                   old_password=old_password,
                                                   new_password=new_password,
                                                   confirm_password=confirm_password))
    if not pmm.old_password_check():
        flash('Error: 密码错误!')
        pmm.session_close()
        return redirect(url_for('change_password', user_code=user_code, old_password=' ', new_password=new_password,
                                confirm_password=confirm_password))
    if not pmm.new_password_check():
        flash('Error: 前后密码不一致!')
        pmm.session_close()
        return redirect(url_for('change_password', user_code=user_code, old_password=old_password, new_password=' ',
                                confirm_password=' '))

    pmm.user_password_modify()

    flash('Success: 密码修改成功!')
    pmm.session_close()
    return redirect(url_for('change_password', user_code=' ', old_password=' ', new_password=' ',
                            confirm_password=' '))


if __name__ == '__main__':
    app.run(debug=True)
