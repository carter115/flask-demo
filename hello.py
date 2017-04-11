#!/usr/bin/env python
# coding=utf-8
import sys, os

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, url_for, abort, redirect, session, flash
from flask_script import Manager
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
from flask_mail import Mail
from flask_mail import Message

from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField, SelectMultipleField
from wtforms.validators import Required, DataRequired, IPAddress

basedir = os.path.dirname(__file__)



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydata.db')

app.config['MAIL_SERVER'] = 'smtp.139.com'
app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '15920405043@139.com'
app.config['MAIL_PASSWORD'] = 'abcd'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <15920405043@139.com>'


bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)
mail=Mail(app)




class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship("User",backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role: %s>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s>' % self.username


class NameForm(FlaskForm):
    name = StringField('帐号', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('提交')


class BookForm(FlaskForm):
    name = StringField('姓名', validators=[Required()])
    phone = IntegerField('号码', validators=[Required()])
    phoneset = SelectMultipleField('类型', choices=[('SET1', 135), ('SET2', 137)])
    submit = SubmitField('预定')


@app.route("/", methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
        else:
            flash(u'用户已存在.')
        session['name'] = form.name.data
        session['password'] = form.password.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), password=session.get('password'))


@app.route('/book', methods=['POST', 'GET'])
def book():
    # name, phone, phoneset = (None, None, None)
    form = BookForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你的用户已发生变化.')
        session['name'] = form.name.data
        session['phone'] = form.phone.data
        session['phoneset'] = form.phoneset.data
        return redirect(url_for('book'))
    return render_template('book.html', form=form, name=session.get('name'), phone=session.get('phone'),
                           phoneset=session.get('phoneset'))


@app.route('/user/<name>')
def user(name):
    # return "<h1>Hello %s !</h1>" % name
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

from flask_script import Shell

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

if __name__ == "__main__":
    manager.run()

    # http://www.tuicool.com/articles/YF7zMbr

# http://doc.iplaypy.com/flask/#tutorial-schema
# https://www.zhihu.com/question/20135205

# 动手写最快，先实现增删改查，再一步一步增加功能。
# 1、增加分页
# 2、增加评论
# 3、增加用户注册、登录、注销。
# 4、增加用户邮件验证、增加验证码。
# 5、增加RESTFUL API