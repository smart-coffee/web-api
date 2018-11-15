from flask import Flask, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from config.environment_tools import init_environment
from config.swagger import get_swagger_template

def create_app(env_path: str):
    app = Flask(__name__)
    CORS(app, allow_headers="*")
    init_environment(env_path=env_path)
    # Configuration should be refactored (e.g. from .env instead of pyfile)
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('development.py')
    return app


def get_db(app: Flask) -> SQLAlchemy:
    return SQLAlchemy(app)


def get_db_session(app: Flask):
    _db = get_db(app)
    return _db.session


def get_secret_key(app: Flask):
    return app.config['SECRET_KEY']


FLASK_APP = create_app(None)
SWAG = Swagger(FLASK_APP, template=get_swagger_template())
DB = get_db(FLASK_APP)