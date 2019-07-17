"""setup auth resource blueprint."""

from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
authenticate = Blueprint('authenticate', __name__)

from . import views



