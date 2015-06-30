from flask_wtf import Form
from wtforms import (StringField, IntegerField, RadioField, TextAreaField)
from wtforms.validators import (InputRequired,NumberRange, Length)

from app.models import Ticket

class TicketForm(Form):
    building_id = IntegerField('building', validators=[InputRequired(), NumberRange(1,3)])
    classroom_id = IntegerField('classroom', validators=[NumberRange(1,3)])
    reporter_contact = StringField('contact')
    description = TextAreaField('description', validators=[InputRequired()])
