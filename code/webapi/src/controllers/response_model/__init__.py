from flask_restful import fields

from config import SWAG


@SWAG.definition('User')
def get_registered_user_details():
    """
    file: /controllers/response_model/user.yml
    """
    _user_fields = {
        'public_id': fields.String,
        'name': fields.String,
        'email': fields.String
    }
    return _user_fields


@SWAG.definition('Role')
def get_role_fields():
    """
    file: /controllers/response_model/role.yml
    """
    _role_fields = {
        'id': fields.Integer,
        'name': fields.String
    }
    return _role_fields


@SWAG.definition('CoffeeMachine')
def get_coffee_machine_fields():
    """
    file: /controllers/response_model/coffee_machine.yml
    """
    _coffee_machine_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'repository': fields.String
    }
    return _coffee_machine_fields


@SWAG.definition('CoffeeType')
def get_coffee_type_fields():
    """
    file: /controllers/response_model/coffee_type.yml
    """
    _coffee_type_fields = {
        'id': fields.Integer,
        'name': fields.String
    }
    return _coffee_type_fields


@SWAG.definition('Token')
def get_token_fields():
    """
    file: /controllers/response_model/token.yml
    """
    _token_fields = {
        'token': fields.String
    }
    return _token_fields


@SWAG.definition('CoffeeBrand')
def get_coffee_brand_fields():
    """
    file: /controllers/response_model/coffee_brand.yml
    """
    _coffee_brand_fields = {
        'id': fields.Integer,
        'name': fields.String
    }
    return _coffee_brand_fields


@SWAG.definition('CoffeeProduct')
def get_coffee_product_fields():
    """
    file: /controllers/response_model/coffee_product.yml
    """
    _coffee_product_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'coffee_brand_id': fields.Integer,
        'coffee_type_id': fields.Integer
    }
    return _coffee_product_fields