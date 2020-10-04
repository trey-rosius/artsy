from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Length(min=6, max=35)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')
