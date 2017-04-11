#!/usr/bin/env python
#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('帐号', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('提交')