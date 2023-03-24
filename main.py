# -*- coding: utf-8 -*-
'''
    命名规范：D_——与医生相关    M_——与管理员相关
            _log——登录相关
'''
from flask import Flask, url_for, redirect, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo

import people_db
import doctor_db
import manager_db

app = Flask(__name__)
app.secret_key = 'itheima' # 密码加密，必须要

# 初始化为全局变量，用于在同一路径下不同页面间传递数据
'''
    设置默认值逻辑：StringField必须有值提取才能进行跳转，设置默认值，非默认值即为输入
'''
people_data_ID_card = 'xxx'
people_data_name = 'xxx'
people_data_sex='x'
people_data_tele = 'xxx'
people_data_situ = 'xxx'

# 登录界面，输入框类
class LoginForm(FlaskForm):
    ID_Card = StringField(u'身份证号：', validators=[DataRequired()], render_kw={"placeholder": "身份证号"})
    name = StringField(u'姓名：', validators=[DataRequired()], render_kw={"placeholder": "姓名"})
    check = SubmitField(u'查询')
class Doctor_log(FlaskForm):
    id = StringField(u'账号：', validators=[DataRequired()], render_kw={"placeholder": "账号"})
    password = PasswordField(u'密码：', validators=[DataRequired()], render_kw={"placeholder": "密码"})
    log = SubmitField(u'登录')
class Manager_log(FlaskForm):
    id = StringField(u'账号：', validators=[DataRequired()], render_kw={"placeholder": "账号"})
    password = PasswordField(u'密码：', validators=[DataRequired()], render_kw={"placeholder": "密码"})
    log = SubmitField(u'登录')

# 医生增加信息类
class D_op_add_class(FlaskForm):
    ID_card = StringField(u'身份证号：', validators=[DataRequired()])
    name = StringField(u'姓名：', validators=[DataRequired()])
    sex = StringField(u'性别：', validators=[DataRequired()])
    tele = StringField(u'联系电话：', validators=[DataRequired()])
    situ = StringField(u'接种情况：', validators=[DataRequired()])
    add = SubmitField(u'确定')

# 管理员添加信息类（医生账户）
class M_op_add_class(FlaskForm):
    id = StringField(u'账号：', validators=[DataRequired()])
    password = StringField(u'密码：', validators=[DataRequired()])
    add = SubmitField(u'确定')

# 管理员删除信息类（医生账户）
class M_op_delete_class(FlaskForm):
    id = StringField(u'账号：', validators=[DataRequired()])
    delete = SubmitField(u'确定')

# 查询/修改用户信息类
class D_change(FlaskForm):
    new_name = StringField(u'姓名：', validators=[DataRequired()])
    sex = StringField(u'姓别：', validators=[DataRequired()])
    tele = StringField(u'联系方式：', validators=[DataRequired()])
    situ = StringField(u'接种情况：', validators=[DataRequired()])
    change = SubmitField(u'修改')
    change_name = SubmitField(u'修改姓名')
    change_sex = SubmitField(u'修改性别')
    change_tele = SubmitField(u'修改联系方式')
    change_situ = SubmitField(u'修改接种情况')
    delete = SubmitField(u'删除该群众')
    back = SubmitField(u'返回主操作界面')

# 群众登录
@app.route('/', methods = ['GET','POST'])
def people_log():
    login_form = LoginForm()
    if (request.method == 'POST'):
        if login_form.validate_on_submit():
            print('hello')
            ID_Card = request.form.get('ID_Card')
            name = request.form.get('name')
            judge_select = people_db.select(ID_Card, name)
            if judge_select == []:
                flash(u'身份证号或姓名错误')
            else:
                #people_data  = People_data() 使用封装类无法传入赋值参数，改为使用变量传递
                people_data_ID_card = judge_select[0][0]
                people_data_name = judge_select[0][1]
                people_data_sex = judge_select[0][2]
                people_data_tele = judge_select[0][3]
                people_data_situ = judge_select[0][4]
                return render_template("people_op.html", people_data_ID_card=people_data_ID_card, people_data_name=people_data_name,people_data_sex=people_data_sex,people_data_tele=people_data_tele,people_data_situ=people_data_situ)
    return render_template("people_log.html", form=login_form)

# 医生账号登录
@app.route('/doctor_log', methods = ['GET','POST'])
def doctor_log():
    doctor_log = Doctor_log()
    if (request.method == 'POST'):
        if doctor_log.validate_on_submit():
            id = request.form.get('id')
            password = request.form.get('password')
            judge_select = doctor_db.select(id, password)
            if judge_select == []:
                flash(u'账号或密码错误')
            else:
                return render_template("D_op_main.html")
    return render_template("doctor_log.html", doctor_log=doctor_log)

# 管理员登录
@app.route('/manager_log', methods = ['GET','POST'])
def manager_log():
    manager_log = Manager_log()
    if (request.method == 'POST'):
        if manager_log.validate_on_submit():
            id = request.form.get('id')
            password = request.form.get('password')
            judge_select = manager_db.select(id, password)
            if judge_select == []:
                flash(u'账号或密码错误')
            else:
                return render_template("M_op_main.html")
    return render_template("manager_log.html", manager_log=manager_log)

# 管理员操作：添加医生账户
@app.route('/M_op_add', methods = ['GET','POST'])
def M_op_add():
    m_op_add = M_op_add_class()
    if (request.method == 'POST'):
        if m_op_add.validate_on_submit():
            id = request.form.get('id')
            password = request.form.get('password')
            doctor_db.insert(id, password)
            flash(u'添加成功！')
            return render_template("M_op_main.html")
    return render_template("M_op_add.html", m_op_add=m_op_add)

# 管理员操作：查询/修改群众信息
@app.route('/M_op_select1', methods=['GET','POST'])
def M_op_select1():
    # 引用群众登录界面
    global people_data_ID_card,people_data_name,people_data_sex,people_data_situ,people_data_tele
    new_name = None
    new_sex = None
    new_tele = None
    new_situ = None
    login_form = LoginForm()
    # 功能相同，复用D_change类
    m_change = D_change(new_name='xxx', sex='x', situ='xxx',tele='xxx')
    if request.method == 'POST':
        if m_change.change.data:
            # request.from.get没内容返回值为None
            new_name = request.form.get('new_name')
            new_sex = request.form.get('sex')
            new_tele = request.form.get('tele')
            new_situ = request.form.get('situ')
            if new_name != 'xxx':
                people_data_name = new_name
            if new_sex != 'x':
                people_data_sex = new_sex
            if new_tele != 'xxx':
                people_data_tele = new_tele
            if new_situ != 'xxx':
                people_data_situ = new_situ
            people_db.change_data(people_data_ID_card,people_data_name,people_data_sex,people_data_tele,people_data_situ)
            return render_template("M_op_select2.html", m_change=m_change, people_data_ID_card=people_data_ID_card, people_data_name=people_data_name,people_data_sex=people_data_sex,people_data_tele=people_data_tele,people_data_situ=people_data_situ)
        if m_change.delete.data:
            people_db.delete(people_data_ID_card)
            return render_template("M_op_select1.html", form=login_form)
        if m_change.back.data:
            return render_template("M_op_main.html")
        if login_form.validate_on_submit():
            ID_Card = request.form.get('ID_Card')
            name = request.form.get('name')
            judge_select = people_db.select(ID_Card, name)
            if judge_select == []:
                flash(u'身份证号或姓名错误')
            else:
                people_data_ID_card = judge_select[0][0]
                people_data_name = judge_select[0][1]
                people_data_sex = judge_select[0][2]
                people_data_tele = judge_select[0][3]
                people_data_situ = judge_select[0][4]
                return render_template("M_op_select2.html", m_change=m_change, people_data_ID_card=people_data_ID_card, people_data_name=people_data_name,people_data_sex=people_data_sex,people_data_tele=people_data_tele,people_data_situ=people_data_situ)

    return render_template("M_op_select1.html", form=login_form)

# 管理员操作：删除医生账户
@app.route('/M_op_delete', methods=['GET','POST'])
def M_op_delete():
    m_op_delete = M_op_delete_class()
    if (request.method == 'POST'):
        if m_op_delete.validate_on_submit():
            id = request.form.get('id')
            doctor_db.delete(id)
            flash(u"删除成功")
            return render_template("M_op_main.html")
    return render_template("M_op_delete.html", m_op_delete=m_op_delete)

# 医生操作：查询/修改群众信息
@app.route('/D_op_select1', methods=['GET','POST'])
def D_op_select1():
    # 引用群众登录界面
    global people_data_ID_card,people_data_name,people_data_sex,people_data_situ,people_data_tele
    new_name = None
    new_sex = None
    new_tele = None
    new_situ = None
    login_form = LoginForm()
    d_change = D_change(new_name='xxx', sex='x', situ='xxx',tele='xxx')
    if request.method == 'POST':
        if d_change.change.data:
            # request.from.get没内容返回值为None
            new_name = request.form.get('new_name')
            new_sex = request.form.get('sex')
            new_tele = request.form.get('tele')
            new_situ = request.form.get('situ')
            if new_name != 'xxx':
                people_data_name = new_name
            if new_sex != 'x':
                people_data_sex = new_sex
            if new_tele != 'xxx':
                people_data_tele = new_tele
            if new_situ != 'xxx':
                people_data_situ = new_situ
            people_db.change_data(people_data_ID_card,people_data_name,people_data_sex,people_data_tele,people_data_situ)
            return render_template("D_op_select2.html", d_change=d_change, people_data_ID_card=people_data_ID_card, people_data_name=people_data_name,people_data_sex=people_data_sex,people_data_tele=people_data_tele,people_data_situ=people_data_situ)
        if d_change.delete.data:
            people_db.delete(people_data_ID_card)
            return render_template("D_op_select1.html", form=login_form)
        if d_change.back.data:
            return render_template("D_op_main.html")
        if login_form.validate_on_submit():
            ID_Card = request.form.get('ID_Card')
            name = request.form.get('name')
            judge_select = people_db.select(ID_Card, name)
            if judge_select == []:
                flash(u'身份证号或姓名错误')
            else:
                people_data_ID_card = judge_select[0][0]
                people_data_name = judge_select[0][1]
                people_data_sex = judge_select[0][2]
                people_data_tele = judge_select[0][3]
                people_data_situ = judge_select[0][4]
                return render_template("D_op_select2.html", d_change=d_change, people_data_ID_card=people_data_ID_card, people_data_name=people_data_name,people_data_sex=people_data_sex,people_data_tele=people_data_tele,people_data_situ=people_data_situ)

    return render_template("D_op_select1.html", form=login_form)

# 医生操作：添加群众信息
@app.route('/D_op_add', methods=['GET','POST'])
def D_op_add():
    d_op_add = D_op_add_class()
    if request.method == 'POST':
        if d_op_add.validate_on_submit():
            ID_card = request.form.get('ID_card')
            name = request.form.get('name')
            sex = request.form.get('sex')
            tele = request.form.get('tele')
            situ = request.form.get('situ')
            people_db.insert(ID_card, name, sex, tele, situ)
            flash(u'添加成功！')
            return render_template("D_op_main.html")
    return render_template("D_op_add.html", d_op_add=d_op_add)

if __name__ == '__main__':
    app.run()
