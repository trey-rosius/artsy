from flask import Flask,render_template
from flask_assets import Environment,Bundle
from config import Config
from forms.login import LoginForm

app = Flask(__name__)

app.config.from_object(Config)







@app.route('/')
def hello_world():


    loginForm = LoginForm()
    return render_template('auth/login.html',form=loginForm)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8000,debug=True)
