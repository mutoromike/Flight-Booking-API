""" /tests/test_auth.py """
import os
import datetime
from contextlib import contextmanager
from unittest import TestCase
from flask_mail import Mail
import json
from app import db, create_app

class BaseTestCase(TestCase):

    TESTING = True
    MAIL_DEFAULT_SENDER = "sender@sender.com"
    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app.config.from_object(self)
        self.assertTrue(self.app.testing)
        self.mail = Mail(self.app)
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        # This is the user test json data with a predefined email and password

        self.user_data = {
            'username':'chrisevans',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'cpassword': 'J@yd33n'
        }

        self.login_data = {
            'email': 'test@example.com',
            'password': 'J@yd33n'
        }

        self.login_admin = {
            'email': os.getenv('ADMIN_EMAIL'),
            'password': os.getenv('ADMIN_PASSWORD')
        }

        self.flight = {
            'name': 'A596',
            'origin': 'Nairobi',
            'destination': 'Mongolia',
            'date': '12/12/2018',
            'time': '5 PM'
        }

        self.booking = {
            "tickets": 1,
            "flight_id": 1,
            "ticket_type": "economy"
        }
        date = datetime.date.today()
        self.date = {
            "date": str(date)
        }
        self.passport = {
            "image_url": "https://res.cloudinary.com/dd1qfqfag/image/upload/v1563726429/test_user_ic2fdy.jpg"
        }
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
            os.system("python manage.py createadmin")

    def tearDown(self):
        self.ctx.pop()

    def register_user(self, data):
        return self.client().post('api/v1/auth/register', data=json.dumps(data), content_type='application/json' )

    def login_user(self, data):
        return self.client().post('/api/v1/auth/login', data=json.dumps(data), content_type='application/json' )

    def get_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data)
        result = self.login_user(self.login_data)
        data = json.loads(result.data.decode())
        access_token = data['access_token']
        return access_token

    def get_admin_token(self):
        """register and login a user to get an access token"""
        result = self.login_user(self.login_admin)
        data = json.loads(result.data.decode())
        access_token = data['access_token']
        return access_token

    @contextmanager
    def mail_config(self, **settings):
        """
        Context manager to alter mail config during a test and restore it after,
        even in case of a failure.
        """
        original = {}
        state = self.mail.state
        for key in settings:
            assert hasattr(state, key)
            original[key] = getattr(state, key)
            setattr(state, key, settings[key])

        yield
        # restore
        for k, v in original.items():
            setattr(state, k, v)

    def assertIn(self, member, container, msg=None):
        if hasattr(TestCase, 'assertIn'):
            return TestCase.assertIn(self, member, container, msg)
        return self.assertTrue(member in container)

    def assertNotIn(self, member, container, msg=None):
        if hasattr(TestCase, 'assertNotIn'):
            return TestCase.assertNotIn(self, member, container, msg)
        return self.assertFalse(member in container)

    def assertIsNone(self, obj, msg=None):
        if hasattr(TestCase, 'assertIsNone'):
            return TestCase.assertIsNone(self, obj, msg)
        return self.assertTrue(obj is None)

    def assertIsNotNone(self, obj, msg=None):
        if hasattr(TestCase, 'assertIsNotNone'):
            return TestCase.assertIsNotNone(self, obj, msg)
        return self.assertTrue(obj is not None)