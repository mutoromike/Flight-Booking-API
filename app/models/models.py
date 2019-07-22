""" app/models.py
    file to handle creation of models
"""

from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app

from app.models.base import BaseModel
from app import db


class User(BaseModel):

    """
    Model defining user table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(256))
    bookings = db.relationship('Bookings', backref='owner', lazy=True)
    images = db.relationship('Images', order_by='Images.id', cascade="all, delete-orphan")
    is_admin = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, username, email, password, is_admin):
        """
        Initialization of user credentials
        """

        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """

        return Bcrypt().check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS512'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"



class Flights(BaseModel):
    """
    This class defines the flights table
    """

    __tablename__ = 'flights'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    origin = db.Column(db.String(128))
    destination = db.Column(db.String(128))
    date = db.Column(db.String(255))
    time = db.Column(db.String(16384))
    bookings = db.relationship('Bookings', backref='flighter', lazy=True)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    @staticmethod
    def get_all(user_id):
        """
        This method gets all the flights for a given user
        """
        return Events.query.filter_by(created_by=user_id)

    def __repr__(self):
        """
        Return a representation of a flight instance
        """
        return "<Flights: {}>".format(self.name)


class BlacklistToken(BaseModel):
    """
    Token Model for storing blacklisted JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<id: token: {}'.format(self.token)


class Images(BaseModel):
    """
    Model to handle image urls
    """
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(500))
    user = db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        """
        Return a representation of an image instance
        """
        return "<Images: {}>".format(self.image_url)


class Bookings(BaseModel):
    """
    Bookings Model
    """

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.String(64), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    flight_status = db.Column(db.String(120), nullable=False, default='pending')
    number_of_tickets = db.Column(db.Integer, nullable=False, default=1)
    ticket_type = db.Column(db.String(255), nullable=False, default='economy')

    def __init__(self, client_id, flight_id, date, ticket_type, no_of_tickets, status='pending'):
        """Initialize the booking details"""
        self.booking_date = date
        self.client_id = client_id
        self.flight_id = flight_id
        self.flight_status = status
        self.ticket_type = ticket_type
        self.number_of_tickets=no_of_tickets

    def __repr__(self):
        """
        Return a representation of a booking instance
        """
        return 'Bookings: {}'.format(self.id)