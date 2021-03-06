from flask import Blueprint, request, redirect,url_for,render_template,flash, abort, jsonify
from flask.ext.login import login_user, login_required, current_user, logout_user
from app.models import *
from app.forms import *
from datetime import datetime
from sqlalchemy import union, or_
from app.utils import sanitize, send_new_ticket_mail

home = Blueprint('home', __name__)

@home.route('/', methods=['GET','POST'])
def index():
    form = TicketForm(request.form)
    if request.method == 'POST' and form.validate_on_submit:
        ticket = Ticket()
        form.description.data = sanitize(form.description.data)
        form.populate_obj(ticket)
        ticket.save()
        message = "你的报修单号码是 " + str(ticket.id) + "，点击 <a href=\"" + url_for('ticket.view_ticket', ticket_id=ticket.id) + "\">这里</a> 查看。"
        # Send mail
        recipients = []
        for manager in ticket.department.managers:
            if manager.email:
                recipients.append(manager.email)
        if recipients:
            send_new_ticket_mail(recipients, ticket)
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
