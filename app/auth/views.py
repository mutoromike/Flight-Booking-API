""" /app/auth/views.py """

from . import auth

from flask_bcrypt import Bcrypt
from flask import make_response, request, jsonify

from app.models.models import User, BlacklistToken
from app.helpers.auth import authorize, register_details


@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    """Method to handle user registration"""
    # Query to see if the user already exists
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
        user = User(username=username, email=email, password=password)
        user.save()
        response = {'message': 'You registered successfully. Please log in.'}
        # return a response notifying the user that they registered successfully      
    except Exception as e:
        # An error occured, therefore return a string message containing the error
        response = {'message': str(e)}
        return make_response(jsonify(response)), 401
    return make_response(jsonify(response)), 201

@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    """Handle POST request for this view. Url ---> /auth/login"""
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

@auth.route('/api/v1/auth/reset-password', methods=['PUT'])
@authorize
def reset_pass(current_user, user_id):
    """Handle PUT request for this view. Url ---> /api/v2/auth/reset-password"""               
    user = User.query.filter_by(id=user_id).first()
    req = request.get_json()
    npass = req['npassword']
    cpass = req['cnfpassword']
    print(npass)
    # Try to authenticate user id and password fields
    if user.id!=user_id:
         # Users can only edit their passwords
        response = {'message': 'You can only edit your own password'}
        return make_response(jsonify(response)), 401
    if npass!=cpass:
        # Passwords aren't matching. Therefore, we return an error message
        response = {'message': 'Enter matching passwords'}
        return make_response(jsonify(response)), 400
    try:
        # Edit the password
        user.password = Bcrypt().generate_password_hash(npass).decode()
        user.save()
        response = {'message': 'Password changed successfully.'}
    except Exception as e:
        # Create a response containing an string error message
        response = {'message': str(e)}
        # Return a server error using the HTTP Error Code 500 (Internal Server Error)
        return make_response(jsonify(response)), 500
    return make_response(jsonify(response)), 200

@auth.route('/api/v1/auth/logout', methods=['POST'])
@authorize
def logout(current_user, user_id):
    access_token = request.headers.get('Authorization')
    if user_id != User.decode_token(access_token):
        response = {'message': 'An error occured.'}
        return make_response(jsonify(response)), 403       
    try:
        # insert the token
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