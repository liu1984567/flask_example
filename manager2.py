#!/usr/bin/python3
"""
    mamager.py

    Implements the management.
"""

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import User, Role, Post
import os
import logging

logging.basicConfig(filename='log.txt',level=logging.DEBUG)
app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test():
    """run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__': 
    logging.info('manager run start')
    manager.run()
