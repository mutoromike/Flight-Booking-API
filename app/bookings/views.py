from flask import Flask, request, jsonify, abort, make_response, g
from flask.views import MethodView
import datetime

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
        """
            Method to create a flight reservation
        """
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
        date = datetime.date.today()
        try:
            new_booking = Bookings(
                client_id=user_id,
                flight_id=flight_id,
                ticket_type=ticket_type,
                number_of_tickets=no_of_tickets,
                booking_date=str(date),
                flight_status="pending"
            )
            new_booking.save()

            response = {
                "message": "Booking successfully created. You'll " \
                    "receive an email once the reservation is approved",
                "id": new_booking.id
            }
            return make_response(jsonify(response)), 201
        except Exception as e:
            response = {
                "message": str(e)
            }
            return make_response(jsonify(response)), 500 

    @authorize
    def get(self, user_id, current_user, flight_id):
        """
            Method to get all reservations for a flight on a specific
            day.
        """
        data = request.get_json()
        date = data["date"]
        print("the date is ", date)
        try:
            flight = Flights.query.filter_by(id=flight_id).first()
            if not flight:
                response = {"message": "The specified flight could not be found!"}
                return make_response(jsonify(response)), 404
            bookings = Bookings.query.filter(Bookings.flight_id==flight_id, Bookings.booking_date==date).all()
            booking_size = []

            for booking in bookings:
                booking_size.append(booking)
            response = {'number_of_bookings': len(booking_size),
                        'message': "Data retrived successfully"}
            return jsonify(response), 200
        except Exception as e:
            response = {"message": str(e)}
            return make_response(jsonify(response)), 500


class BookingsApproval(MethodView):
    """
        Class to handle Admin Reservations approval
    """

    def put(self, booking_id):
        """
        PUT method to approve booking
        """
        booking = Bookings.query.filter_by(id=booking_id).first()
        if not booking:
            response = {
                "message": "The specified reservation could not be found!"
            }
            return make_response(jsonify(response)), 404
        try:
            booking.flight_status = "approved"
            booking.save()
            response = {"message": "Reservation Successfully approved!"}
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {"message": str(e)}
            return make_response(jsonify(response)), 500


booking_view = BookingsView.as_view('bookings')
booking_approval_view = BookingsApproval.as_view('booking_approval')

booking_blueprint.add_url_rule("/api/v1/booking", view_func=booking_view)
booking_blueprint.add_url_rule('/api/v1/booking/<int:flight_id>', view_func=booking_view)
booking_blueprint.add_url_rule('/api/v1/approve/<int:booking_id>', view_func=booking_approval_view)
