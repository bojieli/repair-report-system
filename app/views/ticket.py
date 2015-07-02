from flask import Blueprint, request, redirect,url_for,render_template,flash, abort, jsonify
from flask.ext.login import login_user, login_required, current_user, logout_user
from app.models import *
from app.forms import *
from datetime import datetime
from sqlalchemy import union, or_
from app.utils import send_assign_ticket_mail, send_close_ticket_mail

ticket = Blueprint('ticket', __name__)

@ticket.route('/all/')
def all():
    tickets = Ticket.query.order_by(Ticket.status.desc()).order_by(Ticket.id.desc())
    return render_template('alltickets.html', tickets=tickets)

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

@ticket.route('/<int:ticket_id>/assign/', methods=['GET', 'POST'])
@login_required
def assign(ticket_id):
    if current_user.role != 'Manager':
        abort(403)
    ticket = Ticket.query.get(ticket_id)
    if not ticket or ticket.status == 'Closed':
        abort(404)
    if current_user.department != ticket.department:
        abort(403)

    form = AssignForm(request.form)
    if request.method == 'POST' and form.validate_on_submit:
        worker_id = form.worker.data
        worker = User.query.get(worker_id)
        if not worker:
            abort(404)
        if worker not in ticket.department.workers:
            abort(403)
        ticket.assign_time = datetime.utcnow()
        ticket.manager = current_user
        ticket.worker = worker
        ticket.status = 'Assigned'
        ticket.save()
        if ticket.worker.email:
            recipients = [ticket.worker.email]
            try:
                send_assign_ticket_mail(recipients, ticket)
            except Exception as e:
                print(e)
        return redirect(url_for('ticket.view_ticket', ticket_id=ticket.id))

    return render_template('assign-ticket.html', form=form, ticket=ticket)

@ticket.route('/<int:ticket_id>/respond/', methods=['GET', 'POST'])
@login_required
def respond(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket or ticket.status == 'Closed':
        abort(404)
    if current_user.department != ticket.department:
        abort(403)
    if current_user.role == 'Worker' and ticket.worker != current_user:
        abort(403)

    form = RespondForm(request.form)
    if request.method == 'POST' and form.validate_on_submit:
        ticket.response = form.response.data
        ticket.respond_time = datetime.utcnow()
        ticket.status = 'Closed'
        ticket.save()
        if ticket.reporter_email:
            recipients = [ticket.reporter_email]
            try:
                send_close_ticket_mail(recipients, ticket)
            except Exception as e:
                print(e)
        return redirect(url_for('ticket.view_ticket', ticket_id=ticket.id))

    return render_template('respond-ticket.html', form=form, ticket=ticket)

@ticket.route('/')
def query_ticket():
    ticket_id = request.args.get('id',type=int)
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        message = "你查找的ticket不存在"
        return render_template('feedback.html', status=False, message= message)
    return render_template('viewticket.html', ticket=ticket)

