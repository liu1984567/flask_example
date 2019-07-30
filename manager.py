#manager.py
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
