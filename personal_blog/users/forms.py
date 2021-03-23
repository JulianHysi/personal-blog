"""Module containing form classes for the users bluepring.

---

Classes
-------
RegistrationForm: child of FlaskForm
    the form used for registering new users
LoginForm: child of FlaskForm
    the form used for loging users in
UpdateAccountForm: child of FlaskForm
    the form used for updating a user profile
RequestResetForm: child of FlaskForm
    the form used for requesting a password reset
ResetPasswordForm: child of FlaskForm
    the form used for resetting the user password
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,\
    ValidationError
from flask_login import current_user
from personal_blog.models import User


class RegistrationForm(FlaskForm):
    """The class used to build the user registration form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    username: StringField
        the user username field, mandatory
    email: StringField
        the user email field, mandatory
    password: PasswordField
        the user password field, mandatory
    confirm_password: PasswordField
        the user password confirm field, mandatory
    submit: SubmitField
        the form submit button

    Methods
    -------
    validate_username(self, username): return None
        raise ValidationError if the username already exists
    validate_email(self, email): return None
        raise ValidationError if the email already exists
    """

    username = StringField('Username', validators=[DataRequired(),
                           Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                             Length(min=5)])
    confirm_password = PasswordField(' Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Raise ValidationError if username is already registered.

        ---

        Parameters
        ----------
        username: str
            the username of the current user being created

        Returns
        -------
        None
        """

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        """Raise ValidationError if email is already registered.

        ---

        Parameters
        ----------
        email: str
            the email of the current user being created

        Returns
        -------
        None
        """

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken!')


class LoginForm(FlaskForm):
    """The class used to build the login form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    email: StringField
        the user email field, mandatory
    password: PasswordField
        the user password field, mandatory
    remember: BooleanField
        the remember me field
    submit: SubmitField
        the form submit button
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    """The class used for building the user update account form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    username: StringField
        the user username field, mandatory
    email: StringField
        the user email field, mandatory
    profile_pic: FileField
        the user profile picture file
    submit: SubmitField
        the form submit button

    Methods
    -------
    validate_username(self, username): return None
        raise ValidationError if username already exists
    validate_email(self, username): return None
        raise ValidationError if emaul already exists
    """

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Update profile picture',
                            validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Raise ValidationError if username already exists.

        If there's already a user with that username, and that user
        is not the current user, raise a ValidationError.

        ---

        Parameters
        ----------
        username: str
            the user username to be validated

        Returns
        -------
        None
        """

        user = User.query.filter_by(username=username.data).first()
        if user and user.username != current_user.username:
            raise ValidationError('Username is already taken!')

    def validate_email(self, email):
        """Raise ValidationError if email already exists.

        If there's already a user with that email, and that user
        is not the current user, raise a ValidationError.

        ---

        Parameters
        ----------
        email: str
            the user email to be validated

        Returns
        -------
        None
        """

        user = User.query.filter_by(email=email.data).first()
        if user and user.email != current_user.email:
            raise ValidationError('Email is already taken!')


class RequestResetForm(FlaskForm):
    """The class used to build the request password reset form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    email: StringField
        the email of the account requesting a password reset
    submit: SubmitField
        the form submit button
    """

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')


class ResetPasswordForm(FlaskForm):
    """The class used to build the user reset password form.

    Inherit from FlaskForm base class.
    Create class variables, which are used as form fields and buttons.

    ---

    Class variables
    ---------------
    password: PasswordField
        the new password
    confirm_password: PasswordField
        the new password, confirmed
    submit: SubmitField
        the form submit button
    """

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset password')
