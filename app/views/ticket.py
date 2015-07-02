from flask import Blueprint, request, redirect,url_for,render_template,flash, abort, jsonify
from flask.ext.login import login_user, login_required, current_user, logout_user
from app.models import *
from app.forms import *
from datetime import datetime
from sqlalchemy import union, or_

ticket = Blueprint('ticket', __name__)

@ticket.route('/my/')
@login_required
def mytickets():
    if current_user.role == 'Manager':
        mytickets = Ticket.query.filter(Ticket.department_id == current_user.department_id)
    else: # Worker
        mytickets = Ticket.query.filter(Ticket.worker_id == current_user.id)

    mytickets = mytickets.order_by(Ticket.status.desc()).order_by(Ticket.id.desc())
    return render_template('mytickets.html', tickets=mytickets)


@ticket.route('/<int:ticket_id>')
def view_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        abort(404)
    return render_template('viewticket.html', ticket=ticket)


@ticket.route('/create/')
def create_ticket():
    sanitize(form.content.data)
    return render_template('newticket.html')
