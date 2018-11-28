from flask import Flask

from config.swagger import INDEX_SWAGGER_BP
from config import FLASK_APP
from config.environment_tools import get_cert, get_key
from config.flask_config import FlaskExceptionConfig, post_configuration, register_blueprints

from resources import USER_BP, AUTHENTICATION_BP, ROLE_BP, COFFEE_BP


def start_app(app: Flask):
    _EXCEPTION_CONF = FlaskExceptionConfig(app)
    _blueprints = [
        INDEX_SWAGGER_BP,
        USER_BP,
        AUTHENTICATION_BP,
        ROLE_BP,
        COFFEE_BP
    ]
    _configs = [
        _EXCEPTION_CONF
    ]
    post_configuration(app, _configs)
    register_blueprints(app, _blueprints)

    certificate = get_cert()
    private_key = get_key()
    if certificate and len(certificate) > 0 and not os.path.isfile(certificate):
        raise KeyError('{} does not exist'.format(certificate))
    if private_key and len(private_key) > 0 and not os.path.isfile(private_key):
        raise KeyError('{} does not exist'.format(private_key))
    _ssl_context = (certificate, private_key)
    if not certificate or len(certificate) == 0 or not private_key or len(private_key) == 0:
        _ssl_context = None

    _host = app.config['HOST']
    _port = app.config['PORT']
    _threaded = True
    app.run(host=_host, port=_port, ssl_context=_ssl_context, threaded=_threaded)


if __name__ == '__main__':
    start_app(FLASK_APP)