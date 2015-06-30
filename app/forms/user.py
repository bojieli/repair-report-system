from flask_wtf import Form
from wtforms import (StringField, PasswordField, BooleanField, ValidationError, TextAreaField, FileField, SelectField)
from wtforms.validators import (DataRequired,NumberRange, Email, EqualTo, Length, Optional, AnyOf)
from app.models import User
from flask.ext.login import current_user
from flask.ext.babel import gettext as _
import re

def strip_username(input_s):
    strip_p = re.compile('\s+')
    return strip_p.sub('',input_s)

class UsernameField(StringField):
    ''' a cumstom field of username '''
    def process_data(self,value):
        if value:
            self.data = strip_username(value)
        else:
            self.data = value

class LoginForm(Form):
    username = UsernameField('Username',validators=[DataRequired(), Length(max=30,message='The length must unser 30')])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me',default=False)

