import jwt
import json

from typing import List
from functools import wraps
from flask import Blueprint, request, make_response
from flask_restful import Api
from simplexml import dumps
from werkzeug.wrappers import Response
from werkzeug.http import HTTP_STATUS_CODES
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import class_mapper

from config import get_secret_key, FLASK_APP
from config.flask_config import AuthenticationFailed, ForbiddenResourceException, ResourceException
from models import User, Role
from utils.basic import is_dict_structure_equal


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


def get_delete_response():
    return '', 204


def get_token_response(body, content_type='application/json'):
    if content_type == 'application/json':
        body = json.dumps(body)
    response = Response(body)
    response.status = HTTP_STATUS_CODES[200]
    response.status_code = 200
    response.charset = 'utf-8'
    response.content_type = content_type

    return response


def get_validated_request_body_as_json(template: dict):
    _data = request.get_json()
    if not is_dict_structure_equal(template, _data):
        raise ResourceException('Anfrage enthält unbekannte Wertkombinationen.')
    return _data

def token_required(roles:List[str]=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                raise AuthenticationFailed('Token fehlt.')

            try:
                data = jwt.decode(token, get_secret_key(FLASK_APP), algorithms=['HS256'])
                current_user = User.query.filter_by(
                    public_id=data['public_id']).first()
            except:
                raise AuthenticationFailed('Token ist ungültig.')

            if not (roles is None) and (current_user.role is None or not current_user.role.name in roles):
                raise ForbiddenResourceException('Zugriff verweigert.')

            return func(current_user=current_user, *args, **kwargs)
        return wrapper
    return decorator

def new_alchemy_encoder():
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)
                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields
            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder

def serialize(model, column_filter:dict=None):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    if not column_filter:
        columns = [c.key for c in class_mapper(model.__class__).columns]
    else:
        columns = column_filter.keys()

    # then we return their values in a dict
    values = dict((c, getattr(model, c)) for c in columns)
    return values