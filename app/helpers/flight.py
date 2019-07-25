import re

def validate_data(flight):
    if not flight['name'] or not flight['origin'] or \
    not flight['destination'] or not flight['date'] or not flight['time']:
        return "Flight details cannot be empty!"

    elif not re.match("^[a-zA-Z0-9_ ]*$", flight['name'].strip()):
        return "Flight name cannot have special characters!"

    else:
        return flight