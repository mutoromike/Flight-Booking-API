
def validate_ticket(ticket):
    if not ticket['ticket_type'] or not ticket['flight_id'] or \
    not ticket['tickets']:
        return "Booking details cannot be empty!"

    elif type(ticket['tickets']) is not int:
        return "Number of tickets should be an integer"

    elif type(ticket['flight_id']) is not int:
        return "Flight ID should be an integer"

    elif ticket['tickets'] > 10 or ticket['tickets'] < 1:
        return "You can only book between 1 and 10 tickets" 

    else:
        return ticket