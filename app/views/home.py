from flask import Blueprint, request, redirect,url_for,render_template,flash, abort, jsonify
from flask.ext.login import login_user, login_required, current_user, logout_user
from app.models import User, RevokedToken as RT, Building, Classroom, Ticket
from app.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from app.utils import ts, send_confirm_mail, send_reset_password_mail
from flask.ext.babel import gettext as _
from datetime import datetime
from sqlalchemy import union, or_
from .course import termlist, deptlist

home = Blueprint('home',__name__)

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/tickets/')
def tickets():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tickets_paged = Ticket.query.filter(Ticket.status != 'new').order_by(Ticket.id.desc()).paginate(page=page, per_page=per_page)

    return render_template('tickets.html', tickets=tickets_paged, this_module='home.tickets')

@home.route('/search/')
def search():
    ''' 搜索 '''
    keyword = request.args.get('q')
    if not keyword:
        return redirect(url_for('home.index'))

    classroom_match = Ticket.query.join(Classroom).filter(Classroom.name.like('%' + keyword + '%')).subquery().select()
    description_match = Ticket.query.filter(Ticket.description.like('%' + keyword + '%')).subquery().select()

    tickets = Ticket.query.select_entity_from(union(classroom_match, description_match))
    if not tickets:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tickets_paged = tickets.paginate(page=page, per_page=per_page)

    return render_template('tickets.html', keyword=keyword, tickets=tickets_paged, this_module='home.search')


@home.route('/signin/',methods=['POST','GET'])
def signin():
    next_url = request.args.get('next') or url_for('home.index')
    if current_user.is_authenticated():
        return redirect(next_url)
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user, status, confirmed = User.authenticate(form['username'].data,form['password'].data)
        remember = form['remember'].data
        if user:
            if status:
                return redirect(next_url)
            else:
                error = _('用户名或密码错误！')
        else:
            error = _('用户名或密码错误！')
    return render_template('signin.html',form=form, error=error)





