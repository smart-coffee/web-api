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


@SWAG.definition('CreateCoffeeBrandRequest')
def get_create_coffee_brand_request_fields():
    """
    file: /controllers/request_model/create_coffee_brand_request.yml
    """
    _create_coffee_brand_request_fields = {
        'name': fields.String
    }
    return _create_coffee_brand_request_fields


@SWAG.definition('CreateCoffeeProductRequest')
def get_create_coffee_product_request_fields():
    """
    file: /controllers/request_model/create_coffee_product_request.yml
    """
    _create_coffee_product_request_fields = {
        'name': fields.String,
        'coffee_brand_id': fields.Integer,
        'coffee_type_id': fields.Integer
    }
    return _create_coffee_product_request_fields


@SWAG.definition('CreateCurrentUserProfileRequest')
def get_create_current_user_profile_request_fields():
    """
    file: /controllers/request_model/create_current_user_profile_request.yml
    """
    _create_profile_fields = {
        'name': fields.String,
        'coffee_strength_in_percent': fields.Integer,
        'water_in_percent': fields.Integer
    }
    return _create_profile_fields


@SWAG.definition('EditCurrentUserProfileRequest')
def get_edit_current_user_profile_request_fields():
    """
    file: /controllers/request_model/edit_current_user_profile_request.yml
    """
    _edit_profile_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'coffee_strength_in_percent': fields.Integer,
        'water_in_percent': fields.Integer
    }
    return _edit_profile_fields


@SWAG.definition('CreateJobRequest')
def get_create_job_request_fields():
    """
    file: /controllers/request_model/create_job_request.yml
    """
    _create_job_fields = {
        'coffee_strength_in_percent': fields.Integer,
        'water_in_percent': fields.Integer,
        'price': fields.Integer,
        'doses': fields.Integer,
        'coffee_machine_id': fields.Integer,
        'coffee_product_id': fields.Integer,
        'user_id': fields.String
    }
    return _create_job_fields


@SWAG.definition('EditJobRequest')
def get_edit_job_request_fields():
    """
    file: /controllers/request_model/edit_job_request.yml
    """
    _job_fields = {
        'id': fields.Integer,
        'create_date': fields.Integer,
        'square_date': fields.Integer,
        'coffee_strength_in_percent': fields.Integer,
        'water_in_percent': fields.Integer,
        'price': fields.Integer,
        'doses': fields.Integer,
        'coffee_machine_id': fields.Integer,
        'coffee_product_id': fields.Integer,
        'user_id': fields.String
    }
    return _job_fields


@SWAG.definition('CreateCurrentUserJobRequest')
def get_create_current_user_job_request_fields():
    """
    file: /controllers/request_model/create_current_user_job_request.yml
    """
    _create_job_fields = {
        'coffee_strength_in_percent': fields.Integer,
        'water_in_percent': fields.Integer,
        'price': fields.Integer,
        'doses': fields.Integer,
        'coffee_machine_id': fields.Integer,
        'coffee_product_id': fields.Integer
    }
    return _create_job_fields
