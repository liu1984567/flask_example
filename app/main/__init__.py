# -*- coding: utf-8 -*-
"""
    app.main__init__.py

    Implements the configuration related objects.
"""
from flask import Flask, render_template, session, url_for, flash
from flask import redirect
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import Required
