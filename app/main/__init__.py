"""
    app.main__init__.py

    Implements the configuration related objects.
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

