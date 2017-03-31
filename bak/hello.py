#!/usr/bin/env python
# coding=utf-8
from flask import Flask, render_template, session, redirect, url_for, flash
from datetime import datetime
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_migrate import Migrate,MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from flask import request
from flask import make_response

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

import os
os.getenv('USERNAME')

@app.route("/", methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get("User-Agent")
    # resp = make_response("<h1>Hello World!</h1>  %s" % user_agent)
    # return "<h1>Hello World!</h1>  %s" %user_agent
    # resp.set_cookie("answer", '42')
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            session['known']=False
            user=User(username=form.name.data)
            db.session.add(user)
        else:
            session['known']=True
        form.name.data=''
        return redirect(url_for('index'))
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')
        # name = form.name.data
        # form.name.data = ''
        # session['name'] = form.name.data
        # return redirect(url_for('index'))
    return render_template("index.html", current_time=datetime.utcnow(), form=form, name=session.get('name'),known=session.get('known',False))


@app.route("/user/<name>")
def user(name):
    # return '<h1>Hello World! -- %s </h1>' %name
    return render_template("user.html", name=name)

import sys
sys.argv

if __name__ == '__main__':
    manager.run()
