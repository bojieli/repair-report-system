from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail,Message
from . import app
from flask import render_template, url_for, Markup
from random import randint
from datetime import datetime
import hashlib
import os
from lxml.html.clean import Cleaner
import pytz
import re


mail = Mail(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def rand_str():
    random_num = randint(100000,999999)
    raw_str = str(datetime.utcnow()) + str(randint(100000,999999))
    hash_fac = hashlib.new('ripemd160')
    hash_fac.update(raw_str.encode('utf-8'))
    return hash_fac.hexdigest()

