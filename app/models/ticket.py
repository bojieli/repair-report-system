#!/usr/bin/env python3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
from app import db, login_manager as lm
from random import randint

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def save(self):
        db.session.add(self)
        db.session.commit()

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    name = db.Column(db.String(255))

    department = db.relationship('Department')

    def save(self):
        db.session.add(self)
        db.session.commit()

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    status = db.Column(db.Enum('unassigned', 'assigned', 'closed'), nullable=False, default='unassigned') # 未分配、已分配、已处理
    description = db.Column(db.Text())

    report_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    reporter_email = db.Column(db.String(255))
    reporter_phone = db.Column(db.String(255))

    assign_time = db.Column(db.DateTime())
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    respond_time = db.Column(db.DateTime())
    response = db.Column(db.Text())

    building = db.relationship('Building')
    classroom = db.relationship('Classroom')
    worker = db.relationship('User', foreign_keys=worker_id)

    def save(self):
        db.session.add(self)
        db.session.commit()
