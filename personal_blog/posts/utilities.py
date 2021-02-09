import re
import os


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
