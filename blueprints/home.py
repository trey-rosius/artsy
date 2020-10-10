
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

import pyrebase
import firestore
from forms.login import LoginForm

from forms.register import RegisterForm

bp = Blueprint('home', __name__)



@bp.route('/')
def index():
    items = firestore.load_items()

    return render_template('index.html', items=items)

