"""
A module used to run the application, if called directly

---

Examples
--------
    Change directory to the app's top level directory, and hit the
    following command on your terminal to run the application:

        $ python run.py

Attributes
----------
app : FlaskApp
    the current application instance
"""

from personal_blog import create_app
from personal_blog.config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()
