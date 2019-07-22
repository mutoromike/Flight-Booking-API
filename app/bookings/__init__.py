"""setup bookings resource blueprint."""

from flask import Blueprint

# This instance of a Blueprint that represents the bookings blueprint
booking_blueprint = Blueprint('bookings', __name__)

from . import views
