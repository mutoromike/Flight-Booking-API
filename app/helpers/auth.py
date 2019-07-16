import re
from functools import wraps
from app.models.models import User, BlacklistToken

def authorize(f):
# Function to authenticate users while accessing other pages
    @wraps(f)
    def check(*args, **kwargs):
        """Function to check login status"""
        access_token = request.headers.get('Authorization')
        blacklisted = BlacklistToken.query.filter_by(token=access_token).first()
        user_id = User.decode_token(access_token)

        # Check if the token is blacklisted
        if blacklisted:
            response = {"message": "Logged out. Please login again!" }
            return make_response(jsonify(response)), 401
        # Get user_id from the token
        if not isinstance(user_id, str):
            try:
                current_user = User.query.filter_by(id=user_id).first()
                return f(current_user, user_id, *args, **kwargs)
            except KeyError:
                response = {"message": "One or more event attributes are missing!"}
                return make_response(jsonify(response)), 500
        
        msg = {'message': 'Invalid token or Token has expired! PLEASE LOGIN!'}
        return make_response(jsonify(msg)), 401
    return check


def register_details(data):
    """
        A method that uses regex
        to validate user inputs
    """
    if not re.match("^[a-zA-Z0-9_]*$", data['username']):
        # Check username special characters        
        return 'Username cannot have special characters!'
    if len(data['username'].strip())<5:
        # Checkusername length
        # return an error message if requirement not met
        # return a 403 - auth failed
        return 'Username must be more than 5 characters'
    if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", data['email']):
        # Check email validity
        return 'Provide a valid email!'
    if (data['password']!=data['cpassword']):
        # Verify passwords are matching
        return 'The passwords should match!'
    if len(data['password']) < 5 or not re.search("[a-z]", data['password']) or not\
    re.search("[0-9]", data['password']) or not re.search("[A-Z]", data['password']):
        # Check password strength
        return 'Password length should be more than 5 characters, '\
            'have one number and special character'
    else:
        return data