"""
    mamager.py

    Implements the management.
"""

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import User, Role
import os

app = create_app(os.environ.get('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__': 
    manager.run()
