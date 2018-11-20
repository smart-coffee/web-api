import datetime
import jwt
from flasgger import swag_from
from flask import Blueprint, request
from flask.views import MethodView
from flask_restful import Api
from werkzeug.security import check_password_hash

from models import User
from config.environment_tools import get_secret_key
from controllers.request_model import get_credentials_fields
from config.flask_config import AuthenticationFailed
from utils.basic import is_dict_structure_equal
from utils.http import get_token_response, token_required

from config.logger import logging, get_logger_name


logger = logging.getLogger(get_logger_name(__name__))

API_PREFIX = 'auth'
AUTHENTICATION_BP = Blueprint('{0}_api'.format(API_PREFIX), __name__)
api = Api(AUTHENTICATION_BP)


class LoginAPI(MethodView):
    @swag_from('/resources/authentication/description/login.yml')
    # Causes token=null ?
    # @marshal_with(get_token_fields())
    def post(self):
        data = request.get_json()

        if not is_dict_structure_equal(get_credentials_fields(), data):
            logger.warning('Request body has an unknown structure.')
            raise AuthenticationFailed('Could not verify')

        username = data['username']
        password = data['password']

        if not username or not password:
            logger.warning('Password is missing.')
            raise AuthenticationFailed('Could not verify')
        user = User.query.filter_by(name=username).first()

        if not user:
            logger.warning('User could not be found in database.')
            raise AuthenticationFailed('Could not verify')

        if check_password_hash(user.password, password):
            logger.info('Log in successful: {}'.format(user.public_id))
            token = _generate_token(user)
            return get_token_response(dict(
                token=token.decode('UTF-8')
            ))
        logger.warning('Password is wrong.')
        raise AuthenticationFailed('Could not verify')


class RefreshAPI(MethodView):
    @token_required
    @swag_from('/resources/authentication/description/refresh.yml')
    def post(self, current_user: User):
        token = _generate_token(current_user)
        return get_token_response(dict(
                token=token.decode('UTF-8')
        ))


def _generate_token(user: User):
    public_id = user.public_id
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    secret_key = get_secret_key()
    algorithm = 'HS256'

    token = jwt.encode({'public_id':public_id, 'exp':expires}, secret_key, algorithm=algorithm)
    return token


api.add_resource(LoginAPI, '/{rsc}/login'.format(rsc=API_PREFIX))
api.add_resource(RefreshAPI, '/{rsc}/refresh'.format(rsc=API_PREFIX))
