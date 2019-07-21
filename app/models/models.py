""" app/models.py
    file to handle creation of models
"""

from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app

reserve = db.Table('reserve',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('flight_id', db.Integer, db.ForeignKey('flights.id'))
    )

class User(db.Model):

    """
    Class defining user table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(256))
    flights = db.relationship('Flights', order_by='Flights.id', cascade="all, delete-orphan")
    client = db.relationship('Flights', secondary='reserve', backref=db.backref('reserve', lazy='dynamic'))
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

    def save(self):
        """
        Save a user to the databse
        """

        db.session.add(self)
        db.session.commit()

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



class Flights(db.Model):
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
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def reserved(self, current_user):
        """Check if a user has already RSVP to an event"""
        return self.reserved.filter_by(id=current_user.id).first() is not None

    def create_reservation(self, current_user):
        """ Add a new user to a list of clients"""
        if not self.reserved(current_user):
            self.reserved.append(current_user)
            self.save()
            return "Reservation Created"
        return "You already have a ticket for this flight"

    def save(self):
        """Create and edit a ticket"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """
        This method gets all the flights for a given user
        """
        return Events.query.filter_by(created_by=user_id)

    def delete(self):
        """
        Deletes a given flight
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Return a representation of a flight instance
        """
        return "<Flights: {}>".format(self.name)


class BlacklistToken(db.Model):
    """
    Token Model for storing blacklisted JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, token):
        self.token = token

    def save(self):
        """Save token"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)


class Images(db.Model):
    """
    Model to handle image urls
    """
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(500))
    user = db.Column(db.Integer, db.ForeignKey(User.id))
    
    def save(self):
        """Saves an image URL"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes a given image
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Return a representation of an image instance
        """
        return "<Images: {}>".format(self.image_url)