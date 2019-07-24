""" /app/auth/views.py """

from . import authenticate

from flask_bcrypt import Bcrypt
from flask.views import MethodView
from flask import make_response, request, jsonify, g

from app.models.models import User, BlacklistToken
from app.helpers.auth import authorize, register_details, with_connection


class RegisterUser(MethodView):
    """
        This class handles user registration
    """
    @with_connection
    def post(self, cnn):

        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        user_name = User.query.filter_by(username=data['username']).first()

        username = data['username']
        email = data['email']
        password = data['password']
        cpassword = data['cpassword']
        new_user = register_details(data)
        if new_user is not data:
            # Validate register details
            return jsonify({"message": new_user}), 403
        if user_name:
            # Username already exists.
            response = {'message': 'Username already exists'}
            return make_response(jsonify(response)), 302
        if user:
            # User already exists. Skip registration
            response = {'message': 'User already exists. Please login.'}
            return make_response(jsonify(response)), 199
        # Register the user
        user = User(
                username=username,
                email=email,
                password=password,
                is_admin=False)
        user.save()
        response = {'message': 'You registered successfully. Please log in.'}
        # return a response notifying the user that they registered successfully 
        return make_response(jsonify(response)), 201


class LoginUser(MethodView):
    """
        This class handles user login
    """
    @with_connection
    def post(self, conn):

        # Get the user object using their email (unique to every user)
        req = request.get_json()
        user = User.query.filter_by(email=req['email']).first()

        # Try to authenticate the found user using their password
        if user and user.password_is_valid(req['password']):
            # Generate the access token. This will be used as the authorization header
            access_token = user.generate_token(user.id)
            if access_token:
                g.current_user = user
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token.decode()
                }
                return make_response(jsonify(response)), 200
        else:
            # User does not exist. Therefore, we return an error message
            response = {'message': 'Invalid email or password, Please try again'}
            return make_response(jsonify(response)), 401


class LogoutUser(MethodView):
    """
        This class handles user LOGOUT
    """

    @with_connection
    def post(self, conn):

        header = request.headers.get('Authorization')
        if header:
            access_token = header.split(" ")[0]
        else:
            access_token = ''
        if access_token:
            value = User.decode_token(access_token)
            if not isinstance(value, str):
                # mark token as blacklisted
                token = BlacklistToken.query.filter_by(token=access_token).first()
                if token:
                    response = {
                        'message': 'You have been logged out already!'
                    }
                    return make_response(jsonify(response)), 401

                blacklist_token = BlacklistToken(token=access_token)
                blacklist_token.save()
                response = {
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Failed! Auth token corrupt!'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response)), 403


registration_view = RegisterUser.as_view('register')
login_view = LoginUser.as_view('login')
logout_view = LogoutUser.as_view('logout')


authenticate.add_url_rule('/api/v1/auth/register', view_func=registration_view)
authenticate.add_url_rule('/api/v1/auth/login', view_func=login_view)
authenticate.add_url_rule('/api/v1/auth/logout', view_func=logout_view)