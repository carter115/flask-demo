#!/usr/bin/env python
#coding=utf-8
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config

bootstrap=Bootstrap()
mail=Mail()
moment=Moment()
db=SQLAlchemy()

