#!/usr/bin/env python3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
from app import db, login_manager as lm
from random import randint
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask.ext.babel import gettext as _

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255), unique=True) #用户名
    password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.Enum('Reporter', 'Manager', 'Worker'), nullable=False) # 报修用户、维修部门主管、维修人员
    contact = db.Column(db.String(255))  # 联系方式

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<{} {} ({})>'.format(self.role, self.username, self.password)

    def save(self):
        db.session.add(self)
        db.session.commit()


@lm.user_loader
def load_user(userid):
    return User.query.get(userid)
