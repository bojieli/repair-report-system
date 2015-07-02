from flask import Blueprint, request, redirect,url_for,render_template,flash, abort, jsonify
from flask.ext.login import login_user, login_required, current_user, logout_user
from app.models import *
from app.forms import *
from datetime import datetime
from sqlalchemy import union, or_

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/tickets/')
def tickets():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tickets_paged = Ticket.query.order_by(Ticket.id.desc()).paginate(page=page, per_page=per_page)

    return render_template('tickets.html', tickets=tickets_paged, this_module='home.tickets')

@home.route('/search/')
def search():
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

