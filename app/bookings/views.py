from flask import Flask, request, jsonify, abort, make_response, g
from flask.views import MethodView

from . import flight_blueprint
from app.models.models import Flights, User, BlacklistToken
from app.helpers.flight import validate_data
from app.helpers.auth import authorize, check_user_role

import re