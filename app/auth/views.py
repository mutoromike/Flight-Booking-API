""" /app/auth/views.py """

from . import authenticate

from flask_bcrypt import Bcrypt
from flask.views import MethodView
from flask import make_response, request, jsonify

from app.models.models import User, BlacklistToken
from app.helpers.auth import authorize, register_details


class RegisterUser(MethodView):
    """
    This class handles user registration
    """

    def post(self):

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
        try:
            # Register the user
            user = User(
                    username=username,
                    email=email,
                    password=password)
            user.save()
            response = {'message': 'You registered successfully. Please log in.'}
            # return a response notifying the user that they registered successfully      
        except Exception as e:
            # An error occured, therefore return a string message containing the error
            response = {'message': str(e)}
            return make_response(jsonify(response)), 401
        return make_response(jsonify(response)), 201


class LoginUser(MethodView):
    """
    This class handles user login
    """

    def post(self):

        try:
            # Get the user object using their email (unique to every user)
            req = request.get_json()
            user = User.query.filter_by(email=req['email']).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(req['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {'message': 'Invalid email or password, Please try again'}
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {'message': str(e)}
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500


class LogoutUser(MethodView):
    """
    This class handles user LOGOUT
    """

    def post(self):

        header = request.headers.get('Authorization')
        if header:
            access_token = header.split(" ")[0]
        else:
            access_token = ''
        if access_token:
            value = User.decode_token(access_token)
            if not isinstance(value, str):
                try:
                    # mark token as blacklisted
                    blacklist_token = BlacklistToken(token=access_token)
                    blacklist_token.save()
                    response = {
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(response)), 200
                except Exception as e:
                    response = {
                        'message': e
                    }
                    return make_response(jsonify(response)), 400
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


authenticate.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST']
)

authenticate.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']
)

authenticate.add_url_rule(
    '/api/v1/auth/logout',
    view_func=logout_view,
    methods=['POST']
)