"""Module containing utility functions for the posts blueprint.

---

Functions
---------
delete_post_images(content, root_path): return None
    delete the image files associated with a post
"""

import re
import os


def delete_post_images(content, root_path):
    """Delete the image files associated with a post.

    Called when the post itself is deleted.
    Build a pattern for matching img src text.
    Use the pattern to search the post's content.
    For every match, build the full filepath of the
    image, and use it to delete the image file.

    ---

    Parameters
    ----------
    content: str
        the contents of the post whose images are to be deleted
    root_path: str
        the root path of the application
    """

    pattern = re.compile(r'src="/files/([^"]+)"')
    matches = pattern.finditer(content)
    for match in matches:
        filename = match.group(1)
        filepath = os.path.join(root_path, 'static/post_images', filename)
        os.remove(filepath)
