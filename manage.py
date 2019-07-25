# manage.py

import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models.models import User

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def createadmin():
    """Runs the command to create an admin user"""
    admin_user = User(
        username=os.getenv('ADMIN_USERNAME'),
        email=os.getenv('ADMIN_EMAIL'),
        password=os.getenv('ADMIN_PASSWORD'),
        is_admin=True
    )
    admin_user.save()

if __name__ == '__main__':
    manager.run()
