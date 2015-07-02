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
    role = db.Column(db.Enum('Manager', 'Worker'), nullable=False) # 维修部门主管、维修人员
    department_id = db.Column(db.ForeignKey('departments.id'))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    department = db.relationship('Department', backref='managers')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<{} {} ({})>'.format(self.role, self.username, self.password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_authenticated(self):
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def check_password(self,password):
        """Check passwords.Returns ture if matchs"""
        if self.password is None:
            return False
        return check_password_hash(self.password,password)

    @classmethod
    def authenticate(cls,login,password):
        user = cls.query.filter(User.username == login).first()

        if user and user.confirmed:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated, user.confirmed if user else False


@lm.user_loader
def load_user(userid):
    return User.query.get(userid)
