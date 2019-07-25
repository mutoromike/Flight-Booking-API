""" app/__init__.py """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from config import app_config



# initialize sql-alchemy
db = SQLAlchemy()
mail = Mail()


def create_app(config_name):
	# Initialize app
	app = Flask(__name__)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	mail.init_app(app)
	cors = CORS(app)
	from app.helpers.auto_mail import background_scheduler

	background_scheduler()
	from .auth import authenticate
	from .flights import flight_blueprint
	from .images import image_blueprint
	from .bookings import booking_blueprint
	app.register_blueprint(authenticate)
	app.register_blueprint(flight_blueprint)
	app.register_blueprint(image_blueprint)
	app.register_blueprint(booking_blueprint)

	return app