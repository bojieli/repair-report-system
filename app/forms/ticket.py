from flask_wtf import Form
from wtforms import (StringField, IntegerField, RadioField, TextAreaField)
from wtforms.validators import (InputRequired,NumberRange, Length)

from app.models import Ticket

class TicketForm(Form):
    department_id = IntegerField('building', validators=[InputRequired()])
    location = StringField('location')
    reporter_email = StringField('email')
    reporter_phone = StringField('phone')
    description = TextAreaField('description', validators=[InputRequired()])

class RespondForm(Form):
    response = TextAreaField('response', validators=[InputRequired()])

class AssignForm(Form):
    worker = IntegerField('worker', validators=[InputRequired()])
