from flask import Blueprint,render_template,abort,redirect,url_for,request, abort, flash
from app.models import *
from app.forms import *
from flask.ext.login import login_user, current_user, login_required, logout_user
import re


user = Blueprint('user', __name__)

@user.route('/signin/',methods=['POST','GET'])
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


@user.route('/logout/', methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
