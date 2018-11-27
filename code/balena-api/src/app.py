import os
import sys

from balena import Balena
from flask import Flask, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

from devices import get_devices_api

load_dotenv(find_dotenv())
balena = Balena()
token = os.environ['BALENA_TOKEN']
username = os.environ['BALENA_USERNAME']
password = os.environ['BALENA_PASSWORD']
if token and len(token) > 0:
    print('Login with token.')
    balena.auth.login_with_token(token)
elif username and len(username) > 0 and password and len(password) > 0:
    print('Login with username and password.')
    credentials = {'username':username, 'password':password}
    balena.auth.login(**credentials)
else:
    sys.exit('Use the environment variable "BALENA_TOKEN" to provide an access token to login to the balena API.\
            \nUse the environment variables "BALENA_USERNAME" and "BALENA_PASSWORD" to login without an access token.')

app = Flask(__name__)
CORS(app, allow_headers="*")
app.register_blueprint(get_devices_api, url_prefix='/balena')

if __name__ == '__main__':
    app.run(host=os.environ['APP_HOST'], port=os.environ['APP_PORT'], ssl_context=None, threaded=True)
    