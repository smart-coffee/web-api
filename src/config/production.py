from config.database import get_connection_uri_from_env

ENV = "production"
DEBUG = False
PROPAGATE_EXCEPTIONS = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = get_connection_uri_from_env()

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#configuration-keys
# https://docs.sqlalchemy.org/en/13/core/engines.html#engine-creation-api
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy.create_engine
SQLALCHEMY_ENGINE_OPTIONS = {
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#timeouts
    "pool_recycle" : 500,
    # https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects
    "pool_pre_ping": True
}