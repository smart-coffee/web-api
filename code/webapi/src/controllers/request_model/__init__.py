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


@SWAG.definition('EditUserRequest')
def get_edit_user_request_fields():
    """
    file: /controllers/request_model/edit_user_request.yml
    """
    _user_request_fields = {
        'name': fields.String,
        'email': fields.String,
        'new_password': fields.String,
        'old_password': fields.String
    }
    return _user_request_fields


@SWAG.definition('RegisterUserRequest')
def get_register_user_request_fields():
    """
    file: /controllers/request_model/register_user_request.yml
    """
    _user_request_fields = {
        'name': fields.String,
        'email': fields.String,
        'password': fields.String
    }
    return _user_request_fields


@SWAG.definition('CreateCoffeeMachineRequest')
def get_create_coffee_machine_request_fields():
    """
    file: /controllers/request_model/create_coffee_machine_request.yml
    """
    _create_coffee_machine_request_fields = {
        'name': fields.String,
        'repository': fields.String
    }
    return _create_coffee_machine_request_fields


@SWAG.definition('CreateCoffeeTypeRequest')
def get_create_coffee_type_request_fields():
    """
    file: /controllers/request_model/create_coffee_type_request.yml
    """
    _create_coffee_type_request_fields = {
        'name': fields.String
    }
    return _create_coffee_type_request_fields