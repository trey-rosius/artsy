from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField,FileField,SubmitField,TextAreaField

from wtforms.validators import DataRequired,Length


class ProfileForm(FlaskForm):
    full_names = StringField('Full Names', validators=[DataRequired(), Length(min=6, max=200)])
    email = StringField('Email',validators=[DataRequired(), Length(min=6, max=35)])
    phone_number = StringField('Phone Numbers', validators=[DataRequired(), Length(min=6, max=35)])
    address = TextAreaField('Address', validators=[DataRequired(),Length(min=6, max=200)])
    photo = FileField(validators=[FileRequired()])

    submit = SubmitField('Update Profile')