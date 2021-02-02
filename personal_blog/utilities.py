import re
import os
from PIL import Image
import secrets


def save_profile_picture(profile_pic, app):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(profile_pic.filename)
    filename = random_hex + f_ext  # the name with which it will be saved
    filepath = os.path.join(app.root_path, 'static/profile_pics', filename)

    file_dimensions = (125, 125)  # force these dimensions into the saved file
    image = Image.open(profile_pic)
    image.thumbnail(file_dimensions)

    image.save(filepath)
    return filename


def delete_old_profile_picture(current_user, app):
    filename = current_user.profile_pic
    if filename == 'default.png':
        return  # don't delete default.png, it's needed for new users
    filepath = os.path.join(app.root_path, 'static/profile_pics', filename)
    try:
        os.remove(filepath)
    except:
        pass


#receives the post as parameter, adds appropriate img tags if needed,
# and returns the new content
def add_image_tags(content):
    pattern = re.compile(r'pic\d+')
    # matches every occurence of 'pic' followed by one or more digits
    matches = pattern.finditer(content)
    match_count = 0
    for match in matches:
        match_count += 1
        matched_phrase = match.group(0)
        # group(0) returns the entire match phrase
        new_phrase = '<img src="smiley.gif" alt="image">' #to be completed
        content = content.replace(matched_phrase, new_phrase, 1)
    return content


def save_post_images(images, app):
    for image in images:
        if image.filename:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(image.filename)
            filename = random_hex + f_ext
            # the name with which the file picture will be saved
            filepath = os.path.join(app.root_path, 'static/post_images',
                    filename)

            image_obj = Image.open(image)
            image_obj.save(filepath)
