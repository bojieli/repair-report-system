from flask import Blueprint,render_template,abort,redirect,url_for,request, abort, flash
from app.models import *
from app.forms import *
from flask.ext.login import login_user, current_user, login_required, logout_user
import re


user = Blueprint('user', __name__)


