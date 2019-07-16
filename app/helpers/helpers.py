
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
    re.search("[0-9]", data['password']) or not re.search("[A-Z]", data['password']) \
    or not re.search("[$#@]", data['password']):
        # Check password strength
        return 'Password length should be more than 5 characters, '\
            'have one number and special character'
    else:
        return data