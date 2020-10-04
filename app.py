from flask import Flask, render_template
from flask_assets import Environment, Bundle
from config import Config
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)

app.config.from_object(Config)


@app.route('/login')
def login():
    loginForm = LoginForm()
    return render_template('auth/login.html', form=loginForm)


@app.route('/register')
def register():
    registerForm = RegisterForm()
    return render_template('auth/Register.html', form=registerForm)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8000, debug=True)
