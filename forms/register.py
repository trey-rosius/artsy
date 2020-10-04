from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length

class RegisterForm(FlaskForm):
    full_names = StringField('Full Names', validators=[DataRequired(), Length(min=6, max=200)])
    email = StringField('Email',validators=[DataRequired(), Length(min=6, max=35)])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Register')
