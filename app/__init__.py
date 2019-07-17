""" app/__init__.py """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
	# Initialize app
	app = Flask(__name__)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	cors = CORS(app)

	from .auth import authenticate
	# from .events import events
	app.register_blueprint(authenticate)
	# app.register_blueprint(events)

	return app