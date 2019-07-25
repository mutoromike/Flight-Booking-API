""" app/flights/views.py """

from flask import Flask, request, jsonify, abort, make_response
from flask.views import MethodView

from . import flight_blueprint
from app.models.models import Flights
from app.helpers.flight import validate_data
from app.helpers.auth import authorize, check_user_role, with_connection


class FlightsView(MethodView):
    """
        This class handles flight details:
            :Creation and Fetching flights (by users)
    """

    @with_connection
    @authorize
    @check_user_role
    def post(self, user_id, current_user, conn):
        """
            Method to create flight.
        """

        flight = request.get_json()
        name = flight['name'].strip()
        origin = flight['origin']
        destination = flight['destination']
        date = flight['date']
        time = flight['time']
        new_flight = validate_data(flight)
        if new_flight is not flight:
            return jsonify({"message":new_flight}), 400

        existing = Flights.query.filter_by(name=name).first()
        if existing:
            response = {"message" : "A similar flight already exists!"}
            return make_response(jsonify(response)), 302
        created_flight = Flights(name=name, origin=origin, destination=destination,
        date=date, time=time, created_by=user_id)
        created_flight.save()
        response = jsonify({
            'id': created_flight.id, 'name' : created_flight.name, 'origin' : created_flight.origin,
            'destination' : created_flight.destination, 'date' : created_flight.date,
            'time' : created_flight.time, 'created_by' : created_flight.created_by,
            'message': 'Flight successfully created'
        })                    
        return make_response(response), 201
    
    @authorize
    @check_user_role
    def get(self, user_id, current_user):
        """
            Method to get all flights created by
            the current Admin
        """

        flights = Flights.query.filter_by(created_by=user_id).all()
        results = []

        for flight in flights:
            obj = {
                'id': flight.id, 'name' : flight.name, 'origin' : flight.origin,
                'destination' : flight.destination, 'date' : flight.date, 'time' : flight.time
            }
            results.append(obj)
        return make_response(jsonify(results)), 200

    


class AdminFlightView(MethodView):
    """
        This Class handles Getting and Updating
        a Single Flight
    """

    @authorize
    @check_user_role
    def get(self, user_id, current_user, flight_id):
        """
        Method to Get a specific flight created by a specific User
        """

        flight = Flights.query.filter_by(id=flight_id).first()
        if not flight:
            response = {"message": "The specified FLIGHT does not exist!"}
            return jsonify(response), 404

        else:
            # Handle GET request, sending back the details to the user
            response = {
                'id': flight.id, 'name' : flight.name, 'origin' : flight.origin,
                'destination' : flight.destination, 'date' : flight.date, 'time' : flight.time
            }
            return make_response(jsonify(response)), 200

    @authorize
    @check_user_role
    def put(self, user_id, current_user, flight_id):
        """
            Method to edit flight details
        """

        flight = Flights.query.filter_by(id=flight_id).first()
        created_by = flight.created_by
        if user_id == created_by:
        # Obtain the new name of the flight from the request data
            edited = request.get_json()
            flight.name = edited['name']
            flight.origin = edited['origin']
            flight.location = edited['destination']
            flight.date = edited['date']
            flight.time = edited['time']
            flight.save()

            response = {
                'id': flight.id, 'name' : flight.name, 'origin' : flight.origin,
                'destination' : flight.destination, 'date' : flight.date, 'time' : flight.time
            }

            msg = {"message": "Flight details updated successfully"}
            return make_response(jsonify(msg)), 200
        response = {"message": "You can only modify the flights you created"}
        return jsonify(response), 401


class GetFlights(MethodView):
    """
        Method to get all flights in the system
    """

    def get(self):
        flights = Flights.query.all()
        results = []
        for flight in flights:
            obj = {
                'id': flight.id, 'name' : flight.name, 'origin' : flight.origin,
                'destination' : flight.destination, 'date' : flight.date, 'time' : flight.time
            }
            results.append(obj)
        return make_response(jsonify(results)), 200
flights_view = FlightsView.as_view('flights')
update_flight_view = AdminFlightView.as_view('update_flight')
all_flights_view = GetFlights.as_view('all_flights')

flight_blueprint.add_url_rule('/api/v1/flights', view_func=flights_view)
flight_blueprint.add_url_rule('/api/v1/flight/<int:flight_id>', view_func=update_flight_view)
flight_blueprint.add_url_rule('/api/v1/flights/all', view_func=all_flights_view)
