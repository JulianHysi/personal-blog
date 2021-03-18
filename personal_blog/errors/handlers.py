"""Module containing error handler route functions.

---

Functions
---------
error_403(error): return http response
    the 403 error handler
error_404(error): return http response
    the 404 error handler
error_500(error): return http response
    the 500 error handler
"""

from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
def error_403(error):
    """Error 403 handler route function.

    Render the 403 template, and return the 403 code.
    """

    return render_template('errors/403.html'), 403


@errors.app_errorhandler(404)
def error_404(error):
    """Error 404 handler route function.

    Render the 404 template, and return the 404 code.
    """

    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    """Error 500 handler route function.

    Render the 500 template, and return the 500 code.
    """

    return render_template('errors/500.html'), 500
