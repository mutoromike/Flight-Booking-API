"""setup flights resource blueprint."""

from flask import Blueprint

# This instance of a Blueprint that represents the flights blueprint
flight_blueprint = Blueprint('flights', __name__)

from . import views
