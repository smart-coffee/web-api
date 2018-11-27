import jwt
import json

from functools import wraps
from flask import Blueprint, request, make_response
from flask_restful import Api
from simplexml import dumps
from werkzeug.wrappers import Response, HTTP_STATUS_CODES

from config import get_secret_key, FLASK_APP
from config.flask_config import AuthenticationFailed, ForbiddenResourceException
from models import User


CODE = 201


def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp


def create_custom_api(blueprint: Blueprint) -> Api:
    api = Api(blueprint)
    api.representations['application/xml'] = output_xml
    return api


def get_post_response(obj, body, content_type, api):
    response = Response(body)
    response.status = HTTP_STATUS_CODES[CODE]
    response.status_code = CODE
    response.headers['location'] = '{api}/{new_id}'.format(api=api, new_id=obj.get_id())
    response.autocorrect_location_header = False
    response.content_type = content_type

    return response


def get_token_response(body, content_type='application/json'):
    if content_type == 'application/json':
        body = json.dumps(body)
    response = Response(body)
    response.status = HTTP_STATUS_CODES[200]
    response.status_code = 200
    response.charset = 'utf-8'
    response.content_type = content_type

    return response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            raise AuthenticationFailed('Token is missing')

        try:
            data = jwt.decode(token, get_secret_key(FLASK_APP), algorithms=['HS256'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            raise AuthenticationFailed('Token is invalid')
        return f(current_user=current_user, *args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            raise AuthenticationFailed('Token is missing')

        try:
            data = jwt.decode(token, get_secret_key(FLASK_APP), algorithms=['HS256'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            raise AuthenticationFailed('Token is invalid')

        if current_user.role.name != 'Administrator':
            raise ForbiddenResourceException('Access denied.')

        return f(current_user=current_user, *args, **kwargs)
    
    return decorated
