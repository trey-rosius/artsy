import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json
)

import pyrebase
import firestore
from forms.login import LoginForm

from forms.register import RegisterForm

firebase = pyrebase.initialize_app(json.load(open('firebase_config.json')))


bp = Blueprint('auth', __name__, url_prefix='/auth')





@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user= firestore.readUserInfo(user_id)
# Connect to firebase

@bp.route('/register', methods=('GET', 'POST'))
def register():
    registerForm = RegisterForm()
    auth = firebase.auth()

    if registerForm.validate_on_submit():
        error = None
        if not registerForm.email.data:
            error = "Please enter an email address"
            flash(error)
        elif not registerForm.password.data:
            error = "please enter a password"
        # Get a reference to the auth service
        if error is None:

            try:
                user = auth.create_user_with_email_and_password(registerForm.email.data, registerForm.password.data)

                data = {
                    u'user_id': user['localId'],
                    u'email': user['email'],
                    u'phone_number': '',
                    u'full_names': '',
                    u'address': '',
                    u'login': False

                }
                userRef = firestore.createUserProfile(data, user_id=user['localId'])
                session.clear()
                session['user_id'] = user['localId']
                flash(userRef)
                return redirect('/')
            except Exception as err:
                """Return JSON instead of HTML for HTTP errors."""
                # start with the correct headers and status code from the error
                print(err)
                error = "An error occured while creating the password"

        flash(error)

    return render_template('auth/register.html', form=registerForm)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    loginForm = LoginForm()
    auth = firebase.auth()

    if loginForm.validate_on_submit():
        error = None

        try:
            # Log the user in
            user = auth.sign_in_with_email_and_password(loginForm.email.data, loginForm.password.data)

            data = {
                u'user_id': user['localId'],
                u'email': user['email'],
                u'phone_number':'',
                u'full_names':'',
                u'address':'',
                u'login': True

            }
            userRef = firestore.createUserProfile(data, user_id=user['localId'])
            session.clear()
            session['user_id'] = user['localId']
            flash(userRef)
            return redirect(url_for('profile.update_profile',user_id=user['localId']))
        except Exception as err:
            """Return JSON instead of HTML for HTTP errors."""
            # start with the correct headers and status code from the error
            print(err)
            error = "An error occured while creating the password"

        flash(error)

    return render_template('auth/login.html', form=loginForm)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.list'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


