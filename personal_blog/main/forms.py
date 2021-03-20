"""Module containing form classes for the main blueprint.

---

Classes
-------
SearchForm: child of FlaskForm
    the form used for submitting the search expression
"""

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    """The class used to build the small search form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.
    This form doesn't need a submit button. It will submit on Enter.

    ---

    Class variables
    ---------------
    q: StringField
        the search text field, must be filled in

    Methods
    -------
    __init__(self, *args, **kwargs)
    """

    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Add formdata and disable csrf protection."""
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
