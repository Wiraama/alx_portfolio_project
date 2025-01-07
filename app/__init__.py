""" this module create and controls app """
from flask import Flask
from app.extension import app_extensions
from app.config import config_by_name
from app.error import error_bp
from app.route.main import main
from app.route.auth import auth
from app.extension import db


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flight.db'
    if config_name not in config_by_name:
        raise ValueError(f"Invalid config_name '{config_name}'. Valid option are: {list(config_by_name.keys())}")
    app.config.from_object(config_by_name[config_name])

    # initializing extentions
    app_extensions(app)

    # register Blueprint
    app.register_blueprint(error_bp)
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app
