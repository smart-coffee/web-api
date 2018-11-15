from flask_restful import fields

from config import SWAG


@SWAG.definition('Credentials')
def get_credentials_fields():
    """
    file: /controllers/request_model/credentials.yml
    """
    _credentials_fields = {
        'username': fields.String,
        'password': fields.String
    }
    return _credentials_fields


@SWAG.definition('UserRequest')
def get_user_request_fields():
    """
    file: /controllers/request_model/user_request.yml
    """
    _user_request_fields = {
        'name': fields.String,
        'email': fields.String,
        'new_password': fields.String,
        'old_password': fields.String
    }
    return _user_request_fields