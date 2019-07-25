from flask import Flask, request, jsonify, make_response
from flask.views import MethodView
import datetime

from . import booking_blueprint
from app.models.models import Flights, User, Bookings
from app.helpers.tickets import validate_ticket
from app.helpers.auth import authorize, check_user_role, with_connection
from app.helpers.emails import send_approve

import re


class BookingsView(MethodView):
    """
    Class to handle bookings
    """

    @with_connection
    @authorize
    def post(self, user_id, current_user, conn):
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

    @authorize
    def get(self, user_id, current_user, flight_id):
        """
            Method to get all reservations for a flight on a specific
            day.
        """
        data = request.get_json()
        date = data["date"]
        flight = Flights.query.filter_by(id=flight_id).first()
        if not flight:
            response = {"message": "The specified flight could not be found!"}
            return make_response(jsonify(response)), 404
        bookings = Bookings.query.filter(Bookings.flight_id==flight_id, Bookings.booking_date==date).all()
        if not bookings:
            response = {"message": "Bookings for this flight not found!"}
            return make_response(jsonify(response)), 404
        booking_size = []

        for booking in bookings:
            booking_size.append(booking)
        response = {'number_of_bookings': len(booking_size),
                    'message': "Data retrived successfully"}
        return jsonify(response), 200


class BookingsApproval(MethodView):
    """
        Class to handle Admin Reservations approval
    """
    @with_connection
    @authorize
    @check_user_role
    def put(self, user_id, current_user, conn, booking_id):
        """
        PUT method to approve booking
        """
        booking = Bookings.query.filter_by(id=booking_id).first()
        if not booking:
            response = {
                "message": "The specified reservation could not be found!"
            }
            return make_response(jsonify(response)), 404
        flight_id = booking.flight_id
        user = booking.client_id
        flight = Flights.query.filter_by(id=flight_id).first()
        client = User.query.filter_by(id=user).first()
        booking.flight_status = "approved"
        booking.save()
        send_approve(
            uname=client.username,
            email=client.email,
            name=flight.name,
            origin=flight.origin,
            destination=flight.destination,
            date=flight.date,
            time=flight.time,
            seats=booking.number_of_tickets
        )
        response = {"message": "Reservation Successfully approved!"}
        return make_response(jsonify(response)), 200


class BookingStatus(MethodView):
    """
        Class to handle checking reservation status
    """
    @authorize
    def get(self, user_id, current_user, booking_id):
        """
        GET method to check status
        """
        booking = Bookings.query.filter_by(id=booking_id).first()
        if not booking:
            response = {"message": "The reservation was not found"
            }
            return make_response(jsonify(response)), 404
        flight_id = booking.flight_id
        user = booking.client_id
        if user != user_id:
            response = {"message": "You can only check your own flight status"}
            return make_response(jsonify(response)), 401
        flight = Flights.query.filter_by(id=flight_id).first()
        f_name = flight.name
        status = booking.flight_status
        if status == "pending":
            response = {"message": "Your reservation for Flight " + f_name + \
                " is yet to be approved. You will receive an email when it's approved"
            }
            return make_response(jsonify(response)), 200
        if status == "approved":
            response = {"message": "Your reservation for Flight " + f_name + \
                " is approved! Check your email for the ticket!"
            }
            return make_response(jsonify(response)), 200
        else:
            response = {"message": "Your reservation for Flight " + f_name + \
                " is not yet approved. You'll receive an email once it's done!"
            }
            return make_response(jsonify(response)), 200


booking_view = BookingsView.as_view('bookings')
booking_approval_view = BookingsApproval.as_view('booking_approval')
booking_status_view = BookingStatus.as_view('booking_status')

booking_blueprint.add_url_rule("/api/v1/booking", view_func=booking_view)
booking_blueprint.add_url_rule('/api/v1/booking/<int:flight_id>', view_func=booking_view)
booking_blueprint.add_url_rule('/api/v1/approve/<int:booking_id>', view_func=booking_approval_view)
booking_blueprint.add_url_rule('/api/v1/status/<int:booking_id>', view_func=booking_status_view)
