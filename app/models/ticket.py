#!/usr/bin/env python3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
from app import db, login_manager as lm
from random import randint
from app.models import User

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def managers(self):
        return User.query.filter(User.department_id == self.id).filter(User.role == 'Manager').all()

    @property
    def workers(self):
        return User.query.filter(User.department_id == self.id).filter(User.role == 'Worker').all()



class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    status = db.Column(db.Enum('Unassigned', 'Assigned', 'Closed'), nullable=False, default='Unassigned') # 未分配、已分配、已处理
    location = db.Column(db.String(255))
    description = db.Column(db.Text())

    report_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    reporter_email = db.Column(db.String(255))
    reporter_phone = db.Column(db.String(255))

    assign_time = db.Column(db.DateTime())
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    respond_time = db.Column(db.DateTime())
    response = db.Column(db.Text())

    department = db.relationship('Department')
    manager = db.relationship('User', foreign_keys=manager_id)
    worker = db.relationship('User', foreign_keys=worker_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def status_label(self):
        if self.status == 'Unassigned':
            return '<span class="label label-default">待处理</span>'
        elif self.status == 'Assigned':
            return '<span class="label label-primary">处理中</span>'
        else:
            return '<span class="label label-success">已处理</span>'

