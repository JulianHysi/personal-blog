"""Module containing form classes for the books blueprint.

---

Classes
-------
BookForm: child of FlaskForm
    the form used to add/update books
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    """The class used to build the book form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    title: StringField
        the book title field
    authors: StringField
        the book authors field
    edition: StringField
        the book edition field
    link: StringField
        the book link field
    description: TextAreaField
        the book description/evaluation field
    submit: SubmitField
        the submit button
    """

    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    edition = StringField('Edition', validators=[DataRequired()])
    link = StringField('Link')
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')
