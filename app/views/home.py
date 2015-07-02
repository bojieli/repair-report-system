from flask import Blueprint, request, redirect,url_for,render_template,flash, abort, jsonify
from flask.ext.login import login_user, login_required, current_user, logout_user
from app.models import *
from app.forms import *
from datetime import datetime
from sqlalchemy import union, or_
from app.utils import sanitize

home = Blueprint('home', __name__)

@home.route('/', methods=['GET','POST'])
def index():
    form = TicketForm(request.form)
    if request.method == 'POST' and form.validate_on_submit:
        ticket = Ticket()
        form.description.data = sanitize(form.description.data)
        form.populate_obj(ticket)
        ticket.save()
        message = "你的表单号码是" + str(ticket.id)
        return render_template('feedback.html', status = True, message=message)
    departments = Department.query.all()
    return render_template('index.html',form=form, departments=departments)

@home.route('/signin/',methods=['POST','GET'])
def signin():
    next_url = request.args.get('next') or url_for('home.index')
    if current_user.is_authenticated():
        return redirect(next_url)
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user, status = User.authenticate(form['username'].data,form['password'].data)
        if user:
            if status:
                login_user(user)
                return redirect(next_url)
            else:
                error = '用户名或密码错误！'
        else:
            error = '用户名或密码错误！'
    return render_template('signin.html',form=form, error=error)


@home.route('/logout/', methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
