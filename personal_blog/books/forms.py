from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    edition = StringField('Edition', validators=[DataRequired()])
    link = StringField('Link')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')
