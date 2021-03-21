"""Module containing form classes for the posts blueprint.

---

Classes
-------
PostForm: child of FlaskForm
    the form used for creating/editing posts
CommentForm: child of FlaskForm
    the form used for creating comments
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """The class used to build the post form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    title: StringField
        the post title field, mandatory
    tags: StringField
        the post's tags, mandatory
    content: CKEditorField
        the post contents, mandatory
    submit: SubmitField
        the form submit button
    """

    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    """The class used to build the comment form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    content: TextAreaField
        the comment contents, mandatory
    submit: SubmitField
        the form submit button
    """
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')
