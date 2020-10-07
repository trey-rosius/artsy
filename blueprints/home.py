
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

import pyrebase
import firestore
from forms.login import LoginForm

from forms.register import RegisterForm

firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))


bp = Blueprint('home', __name__)



@bp.route('/')
def list():
    start_after = request.args.get('start_after', None)
    books, last_title = firestore.next_page(start_after=start_after)

    #return render_template('list.html', books=books, last_title=last_title)
    return render_template('empty.html')
