"""setup images resource blueprint."""

from flask import Blueprint

# This instance of a Blueprint that represents the images blueprint
image_blueprint = Blueprint('images', __name__)

from . import views
