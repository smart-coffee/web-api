from config.database import get_connection_uri_from_env

DEBUG = True
ENV = "development"
SQLALCHEMY_DATABASE_URI = get_connection_uri_from_env()
