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

certificate = os.environ['CERT_FILE']
private_key = os.environ['PRIVKEY_FILE']
if certificate and len(certificate) > 0 and not os.path.isfile(certificate):
    raise KeyError('{} does not exist'.format(certificate))
if private_key and len(private_key) > 0 and not os.path.isfile(private_key):
    raise KeyError('{} does not exist'.format(private_key))
_ssl_context = (certificate, private_key)
if not certificate or len(certificate) == 0 or not private_key or len(private_key) == 0:
    _ssl_context = None

if __name__ == '__main__':
    app.run(host=os.environ['APP_HOST'], port=os.environ['APP_PORT'], ssl_context=_ssl_context, threaded=True)
    