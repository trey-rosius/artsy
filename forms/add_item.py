from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField,FileField,SubmitField,TextAreaField

from wtforms.validators import DataRequired,Length


class AddItemForm(FlaskForm):
    name = StringField('Item Description', validators=[DataRequired(), Length(min=6, max=200)])
    desc = TextAreaField('Item Description',validators=[DataRequired(), Length(min=6, max=200)])
    price = StringField('Item Price', validators=[DataRequired(), Length(min=6, max=35)])

    photo = FileField(validators=[FileRequired()])

    submit = SubmitField('Add Item')