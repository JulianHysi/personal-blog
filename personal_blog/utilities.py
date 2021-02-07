import re
import os
from PIL import Image
import secrets
from flask_mail import Message
from flask import url_for
from personal_blog import mail


def save_profile_picture(profile_pic, root_path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(profile_pic.filename)
    filename = random_hex + f_ext  # the name with which it will be saved
    filepath = os.path.join(root_path, 'static/profile_pics', filename)

    file_dimensions = (125, 125)  # force these dimensions into the saved file
    image = Image.open(profile_pic)
    image.thumbnail(file_dimensions)

    image.save(filepath)
    return filename


def delete_old_profile_picture(filename, root_path):
    if filename == 'default.png':
        return  # don't delete default.png, it's needed for new users
    filepath = os.path.join(root_path, 'static/profile_pics', filename)
    try:
        os.remove(filepath)
    except:
        pass


def delete_post_images(content, root_path):
    pattern = re.compile(r'src="/files/([^"]+)"')
    matches = pattern.finditer(content)
    for match in matches:
        filename = match.group(1)
        filepath = os.path.join(root_path, 'static/post_images', filename)
        try:
            os.remove(filepath)
        except:
            pass


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='admin@blog.com',
            recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}  

If you did not make this request, simply ignore this email.
    '''
    mail.send(msg)
