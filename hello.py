#!/usr/bin/env python
# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask, render_template, url_for
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, DataRequired
from flask_script import Manager

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
manager = Manager(app)


@app.route("/")
def index():
    # return redirect('http://test.9yiwu.com')
    # resp=make_response('<h1>This document carries a cookie!</h1>')
    # resp.set_cookie('answer','42')
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


@app.route('/user/<name>')
def user(name):
    # return "<h1>Hello %s !</h1>" % name
    return render_template('user.html', name=name)


@app.route('/book', methods=['POST', 'GET'])
def book():
    name = None
    phone = None
    photoset = None
    booker = BookForm()
    if booker.validate_on_submit():
        name = booker.name.data
        phone = booker.phone.data
        photoset = booker.photoset.data
    return render_template('book.html', form=booker, name=name, phone=phone, photoset=photoset)


@app.route('/temp')
def temp():
    # return url_for("user",name="Tomcat",page=1,status=1,_external=True)
    return url_for('static', filename='css/favicon.ico')


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    # email=StringField('Email Address',[validators.length(min=6,max=25)])
    # password=PasswordField('Password')
    # accept_rules=BooleanField('I accept the site rules',[validators.InputRequired()])
    submit = SubmitField('提交')


class BookForm(Form):
    name = StringField('姓名', validators=[DataRequired()])
    phone = StringField('电话', validators=[DataRequired()])
    photoset = SelectField('套系', choices=[('SET1', '1'), ('SET2', '2')])
    submit = SubmitField("预定")


# class MyForm(Form):
#     name=StringField('name',validators=[DateField()])
#
# @app.route('/submit',methods=['GET','POST'])
# def submit():
#     form=MyForm()
#     if form.validate_on_submit():
#         return redirect('/success')
#     return render_template('submit.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    manager.run()

    # http://www.tuicool.com/articles/YF7zMbr
