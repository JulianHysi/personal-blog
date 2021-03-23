"""The module containing utility functions for the users blueprint.

---

Functions
---------
save_profile_picture(profile_pic, root_path): return str
    the function used to save profile pictures in the filesystem
delete_old_profile_picture(filename, root_path): return None
    the function used to delete the old profile picture
    from the filesystem
send_reset_email(user): return None
    the function used to send a password reset email
"""

import os
import secrets
from threading import Thread

from PIL import Image
from flask_mail import Message
from flask import url_for, current_app

from personal_blog import mail


def save_profile_picture(profile_pic, root_path):
    """Save profile pictures in the filesystem.

    Generate a random hex for the new filename.
    Append to it the extension of the file.
    Build the full filepath of where to save it.
    Force 125x125 dimensions into the file.
    Save it in the filesystem, and return the filename.

    ---

    Parameters
    ----------
    profile_pic: file object
        the image file to be saved
    root_path: str
        the root path of the application

    Returns
    -------
    filename: str
    """

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(profile_pic.filename)
    filename = random_hex + f_ext
    filepath = os.path.join(root_path, 'static/profile_pics', filename)

    file_dimensions = (125, 125)
    image = Image.open(profile_pic)
    image.thumbnail(file_dimensions)

    image.save(filepath)
    return filename


def delete_old_profile_picture(filename, root_path):
    """Delete the old profile picture from the filesystem.

    If the filename is default.png, don't do anything.
    It's the default profile picture that is needed for new users.
    Build the full filepath of the file to be deleted it.
    Use it to delete the file from the filesystem.

    ---

    Parameters
    ----------
    filename: str
        the name of the file to be deleted
    root_path: str
        the root path of the application
    """

    if filename == 'default.png':
        return
    filepath = os.path.join(root_path, 'static/profile_pics', filename)
    os.remove(filepath)


def send_async_email(app, msg):
    """Helper function for send_reset_email()'s threads.

    ---

    Parameters
    ----------
    app: Flask instance
        the current actual application, not a proxy
    msg: Message instance
        the message to be sent via email
    """

    with app.app_context():
        mail.send(msg)


def send_reset_email(user):
    """Send the password reset email.

    Get the reset token from the user who requested the reset.
    Build a Message instance with the subject, sender, and the
    recipients of the email.
    Add do it the body (contents) of the email.
    Send the email via a thread, to not slow down the whole app.

    ---

    Parameters
    ----------
    user: instance of User
        the user to whom the email should be sent
    """

    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='admin@blog.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email.
    '''
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
