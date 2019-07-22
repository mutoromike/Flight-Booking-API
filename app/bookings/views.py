from flask import Flask, request, jsonify, abort, make_response, g
from flask.views import MethodView

from . import booking_blueprint
from app.models.models import Flights, User, Bookings
from app.helpers.tickets import validate_ticket
from app.helpers.auth import authorize

import re


class BookingsView(MethodView):
    """
    Class to handle bookings
    """

    @authorize
    def post(self, user_id, current_user):
        ticket = request.get_json()
        no_of_tickets = ticket['tickets']
        flight_id = ticket["flight_id"]
        ticket_type = ticket["ticket_type"]

        new_ticket = validate_ticket(ticket)
        if new_ticket is not ticket:
            return jsonify({"message":new_ticket}), 400
        existing = Flights.query.filter_by(id=flight_id).first()
        if not existing:
            response = {"message" : "The flight you wish to book doesn't exist"}
            return make_response(jsonify(response)), 400 
        ticket_type = ticket_type.lower()
        try:
            new_booking = Bookings(
                client_id=user_id,
                flight_id=flight_id,
                ticket_type=ticket_type,
                no_of_tickets=no_of_tickets
            )
            new_booking.save()

            response = {"message": "Booking successfully created"}
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {"message": str(e)}
            return make_response(jsonify(response)), 500 




booking_view = BookingsView.as_view('bookings')

booking_blueprint.add_url_rule("/api/v1/booking", view_func=booking_view)
