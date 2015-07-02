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

def send_new_ticket_mail(recipients,ticket):
    subject = "新表单提醒"
    url = url_for('ticket.view_ticket',
        ticket_id=ticket.id,
        _external=True)
    html = render_template('email/new-ticket.html',
            url = url)
    msg = Message(subject=subject, html=html, recipients=recipients)
    mail.send(msg)

def send_assign_ticket_mail(recipients,ticket):
    subject = "分配了新表单"
    url = url_for('ticket.view_ticket',
        ticket_id=ticket.id,
        _external=True)
    html = render_template('email/assign-ticket.html',
            url = url)
    msg = Message(subject=subject, html=html, recipients=recipients)
    mail.send(msg)

def send_close_ticket_mail(recipients,ticket):
    subject = "您提交的保修单已经处理完毕"
    url = url_for('ticket.view_ticket',
        ticket_id=ticket.id,
        _external=True)
    html = render_template('email/close-ticket.html',url=url)
    msg = Message(subject=subject, html=html, recipients=recipients)
    mail.send(msg)

def rand_str():
    random_num = randint(100000,999999)
    raw_str = str(datetime.utcnow()) + str(randint(100000,999999))
    hash_fac = hashlib.new('ripemd160')
    hash_fac.update(raw_str.encode('utf-8'))
    return hash_fac.hexdigest()

def send_confirm_mail(email):
    subject = 'Confirm your email.'
    token = ts.dumps(email, salt='email-confirm-key')

    confirm_url = url_for(
        'home.confirm_email',
        action='confirm',
        token=token,
        _external=True)
    html = render_template('email/activate.html',
            confirm_url = confirm_url)

    msg = Message(subject=subject, html=html, recipients=[email])
    mail.send(msg)

def send_reset_password_mail(email):
    subject = 'Reset your password'
    token = ts.dumps(email, salt='password-reset-key')

    reset_url = url_for(
        'home.reset_password',
        token=token,
        _external=True)
    html = render_template('email/reset-password.html',
            reset_url = reset_url)

    msg = Message(subject=subject, html=html, recipients=[email])
    mail.send(msg)


def allowed_file(filename,type):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'][type]

def handle_upload(file,type):
    ''' type is the file type,for example:image.
    more file type to be added in the future.'''
    if file and allowed_file(file.filename,type):
        old_filename = file.filename
        file_suffix = old_filename.split('.')[-1]
        new_filename = rand_str() + '.' + file_suffix
        try:
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'],type+'s/')
            file.save(os.path.join(upload_path, new_filename))
        except FileNotFoundError:
            os.makedirs(upload_path)
            file.save(os.path.join(upload_path, new_filename))
        except Exception as e:
            return False,e
        return True,new_filename
    return False,"File type disallowd!"


def sanitize(text):
    if text.strip():
        cleaner = Cleaner(safe_attrs_only=False)
        return cleaner.clean_html(text)
    else:
        return text

@app.template_filter('abstract')
def html_abstract(text):
    return Markup(text).striptags()[0:30]

@app.template_filter('localtime')
def localtime_minute(date):
    if not date:
        return 'N/A'
    local = pytz.utc.localize(date, is_dst=False).astimezone(pytz.timezone('Asia/Shanghai'))
    return local.strftime('%Y-%m-%d %H:%M')


