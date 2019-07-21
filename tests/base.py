""" /tests/test_auth.py """
import os

from unittest import TestCase
import json
from app import db, create_app

class BaseTestCase(TestCase):

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
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

        self.passport = {
            "image_url": "https://res.cloudinary.com/dd1qfqfag/image/upload/v1563726429/test_user_ic2fdy.jpg"
        }
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
            os.system("python manage.py createadmin")

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

    def get_new_admin_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.reg_admin2)
        result = self.login_user(self.login_admin2)
        access_token = json.loads(result.data.decode())['access_token']
        return access_token