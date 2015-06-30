#!/usr/bin/env python3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from datetime import datetime
from app import db, login_manager as lm
from random import randint

class Building(db.Model):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Classroom(db.Model):
    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    name = db.Column(db.String(255))

    building = db.relationship('Building')

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))
    report_time = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.Enum('new', 'processing', 'closed')) # 待审核、正在处理、已处理
    reporter_contact = db.Column(db.String(255))
    description = db.Column(db.Text())

    respond_time = db.Column(db.DateTime())
    responser_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    response = db.Column(db.Text())

    building = db.relationship('Building')
    classroom = db.relationship('Classroom')
    responser = db.relationship('User')

