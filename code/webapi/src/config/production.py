from config.database import get_connection_uri_from_env

ENV = "production"
DEBUG = False
PROPAGATE_EXCEPTIONS = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = get_connection_uri_from_env()
