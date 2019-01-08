from config.swagger import get_swagger_spec
from config.environment_tools import get_app_port, get_app_host, get_secret_key

DEBUG = False
TESTING = False
SWAGGER = get_swagger_spec()
SECRET_KEY = get_secret_key()
PORT = get_app_port()
HOST = get_app_host()
