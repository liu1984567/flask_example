"""
    app.auth__init__.py

    Implements the configuration related objects.
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

